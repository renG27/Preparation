from odoo import models, fields, api

class DJBCMutasi(models.Model):
    _name='djbc.mutasi_gb'
    _description='DJBC Laporan Mutasi'
    _rec_name = 'kode_barang'

    sequence = fields.Integer(string='No', readonly=True)
    tgl_mulai = fields.Date(string = 'Tanggal Mulai')
    tgl_akhir = fields.Date(string = 'Tanggal Akhir')
    product_id = fields.Many2one('product.product', string='Product')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    saldo_awal=fields.Float(string='Saldo Awal')
    pemasukan=fields.Float(string='Pemasukan')
    pengeluaran=fields.Float(string='Pengeluaran')
    penyesuaian=fields.Float(string='Penyesuaian')
    stock_opname=fields.Float(string='Stock Opname')
    saldo_akhir=fields.Float(string='Saldo Akhir')
    selisih=fields.Float(string='Selisih')
    keterangan=fields.Char(string='Keterangan')
    location=fields.Char(string='Location')
    satuan=fields.Char(string="Satuan")
    warehouse=fields.Char(string='Warehouse')
    stock_move_lines = fields.One2many(
        'stock.move.line',
        string="Filtered Stock Move Lines",
        compute='_compute_stock_move_lines',
    )
    
    # --- New Summary Fields ---
    total_input_pemasukan = fields.Float(string="Total Input Pemasukan", related='pemasukan', readonly=True)
    sub_total_input_hasil_produksi = fields.Float(string="Sub Total Input Hasil Produksi", readonly=True, default=0.0)
    sub_total_input_pemasukan = fields.Float(string="Sub Total Input Pemasukan", readonly=True, default=0.0)
    total_output_pengeluaran = fields.Float(string="Total Output Pengeluaran", related='pengeluaran', readonly=True)
    sub_total_output_consume_produksi = fields.Float(string="Sub Total Output Consume Produksi", readonly=True, default=0.0)
    sub_total_output_pengeluaran = fields.Float(string="Sub Total Output Pengeluaran", readonly=True, default=0.0)


# --- Field One2many baru untuk setiap tab ---
    input_hasil_produksi_ids = fields.One2many('stock.move.line', compute='_compute_stock_moves', string='Input Hasil Produksi')
    input_pemasukan_ids = fields.One2many('stock.move.line', compute='_compute_stock_moves', string='Input Pemasukan')
    output_consume_produksi_ids = fields.One2many('stock.move.line', compute='_compute_stock_moves', string='Output Consume Produksi')
    output_pengeluaran_ids = fields.One2many('stock.move.line', compute='_compute_stock_moves', string='Output Pengeluaran')
    input_penyesuaian_ids = fields.One2many('stock.move.line', compute='_compute_stock_moves', string='Input Penyesuaian')
    output_penyesuaian_ids = fields.One2many('stock.move.line', compute='_compute_stock_moves', string='Output Penyesuaian')

    @api.depends('product_id', 'tgl_mulai', 'tgl_akhir')
    def _compute_stock_moves(self):
        for rec in self:
            rec.input_hasil_produksi_ids = rec.input_pemasukan_ids = rec.output_consume_produksi_ids = \
            rec.output_pengeluaran_ids = rec.input_penyesuaian_ids = rec.output_penyesuaian_ids = self.env['stock.move.line']
            
            if not (rec.product_id and rec.tgl_mulai and rec.tgl_akhir):
                continue

            domain = [
                ('product_id', '=', rec.product_id.id),
                ('state', '=', 'done'),
                ('date', '>=', rec.tgl_mulai),
                ('date', '<=', rec.tgl_akhir),
            ]
            all_moves = self.env['stock.move.line'].search(domain)

            rec.input_hasil_produksi_ids = all_moves.filtered(lambda m: m.location_id.usage == 'production' and m.location_dest_id.usage == 'internal')
            rec.input_pemasukan_ids = all_moves.filtered(lambda m: m.picking_id.picking_type_id.code == 'incoming')
            rec.output_consume_produksi_ids = all_moves.filtered(lambda m: m.location_id.usage == 'internal' and m.location_dest_id.usage == 'production')
            rec.output_pengeluaran_ids = all_moves.filtered(lambda m: m.picking_id.picking_type_id.code == 'outgoing')
            rec.input_penyesuaian_ids = all_moves.filtered(lambda m: m.location_id.usage == 'inventory' and m.qty_done > 0)
            rec.output_penyesuaian_ids = all_moves.filtered(lambda m: m.location_dest_id.usage == 'inventory' and m.qty_done > 0)

    
    @api.model
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_mutasi_gb(DATE, DATE, INTEGER);
        CREATE OR REPLACE FUNCTION djbc_mutasi_gb(date_start DATE, date_end DATE, v_djbc_category_id INTEGER)
RETURNS VOID AS $BODY$

DECLARE
	v_date_start DATE;
	v_date_end DATE;


BEGIN
	v_date_start = date_start;
	v_date_end = date_end;
	delete from djbc_mutasi_gb;

    insert into djbc_mutasi_gb (product_id, sequence, kode_barang, nama_barang, saldo_awal, pemasukan, pengeluaran, penyesuaian, stock_opname, saldo_akhir, selisih,satuan, keterangan, location, warehouse,tgl_mulai, tgl_akhir)
    select 
    hdr.id as product_id,
    ROW_NUMBER() OVER (ORDER BY hdr.default_code) as sequence,
    hdr.default_code,
    hdr.nama,
    case when sal.saldo is null then 0 else sal.saldo end as saldo,
    case when masuk.masuk is null then 0 else masuk.masuk end as masuk, 
    case when keluar.keluar is null then 0 else keluar.keluar end as keluar, 0.00,0.00,
    case when sal.saldo is null and masuk.masuk is null and keluar.keluar is null then 0  
        when sal.saldo is null and masuk.masuk is null then (0 - keluar.keluar)
        when sal.saldo is null and keluar.keluar is null then masuk.masuk 
        when masuk.masuk is null and keluar.keluar is null then sal.saldo  
        when sal.saldo is null then masuk.masuk-keluar.keluar 
        when masuk.masuk is null then sal.saldo-keluar.keluar 
        when keluar.keluar is null then sal.saldo+masuk.masuk else
        sal.saldo+masuk.masuk-keluar.keluar end as saldo_akhir,
        0.00,
    hdr.satuan,
    ' sesuai','WH/Stock','WH',v_date_start,v_date_end
    from 
    -- Header
    (select 
        pp.id,
        pp.default_code,
        COALESCE(tmp.name->>'en_US', tmp.name->>'id_ID', tmp.name->>0) as nama,
        d.name as kategori,
        COALESCE(uom.name->>'en_US', uom.name->>'id_ID', uom.name->>0) as satuan
    from ( select id,product_tmpl_id,default_code from product_product GROUP BY id ) pp
    left join product_template tmp on pp.product_tmpl_id=tmp.id
    left join djbc_categs d on tmp.djbc_category_id=d.id
    left join uom_uom uom on tmp.uom_id=uom.id
    where tmp.djbc_category_id = v_djbc_category_id
    ) hdr
    left join 
    -- Saldo awal tinggal ganti date
    (select a.product_id as product_id,sum(a.masuk) as saldo from
    (select sm.product_id,sum(sm.product_uom_qty) as masuk from stock_move sm
    left join stock_location sli on sm.location_id=sli.id
    where date(sm.date) < v_date_start and state = 'done' and 
    (sli.location_id=2 or sli.location_id=3)
    group by sm.product_id
    union all
    select sm.product_id,sum(sm.product_uom_qty)*-1 as masuk from stock_move sm
    left join stock_location slo on sm.location_dest_id=slo.id
    where date(sm.date) < v_date_start and state = 'done' and 
    (slo.location_id=2 or slo.location_id=3) 
    group by sm.product_id) a
    group by a.product_id ) sal on hdr.id=sal.product_id
    left join 
    -- Pemasukan
    (select sm.product_id,sum(sm.product_uom_qty) as masuk from stock_move sm
    left join stock_location sli on sm.location_id=sli.id
    where (date(sm.date) >= v_date_start and date(sm.date) <= v_date_end) and state = 'done' and 
    (sli.location_id=2 or sli.location_id=3)
    group by sm.product_id) masuk on hdr.id=masuk.product_id
    left join
    -- Pengeluaran
    (select sm.product_id,sum(sm.product_uom_qty) as keluar from stock_move sm
    left join stock_location slo on sm.location_dest_id=slo.id
    left join stock_picking sp on sm.picking_id = sp.id
    where (date(sm.date) >= v_date_start and date(sm.date) <= v_date_end) and sm.state = 'done' and 
    ((slo.location_id=2 or slo.location_id=3) or sp.picking_type_id = 9)
    group by sm.product_id) keluar on hdr.id=keluar.product_id

    where (case when sal.saldo is null then 0 else sal.saldo end) != 0 OR
          (case when masuk.masuk is null then 0 else masuk.masuk end) != 0 OR
          (case when keluar.keluar is null then 0 else keluar.keluar end) != 0                                                
    ;
END;

$BODY$
LANGUAGE plpgsql;
        """)