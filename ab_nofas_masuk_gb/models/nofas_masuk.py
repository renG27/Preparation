# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)

class DJBCNofasMasuk(models.Model):
    _name = 'djbc.nofas_masuk_gb'
    _description = 'DJBC Laporan Pemasukan'
    _rec_name = 'no_dok'
    _auto = False

        # --- Tambahkan field sequence ---
    sequence = fields.Integer(string='No', readonly=True)
    
    # Existing Fields
    jenis_dok = fields.Char(string='Jenis Dokumen', readonly=True)
    no_dok = fields.Char(string='Nomor Pendaftaran', readonly=True)
    tgl_dok = fields.Date(string='Tgl Pendaftaran', readonly=True)
    no_penerimaan = fields.Char(string='Nomor Penerimaan', readonly=True)
    tgl_penerimaan = fields.Datetime(string='Tgl Penerimaan', readonly=True)
    pengirim = fields.Char(string='Pengirim Barang', readonly=True)
    kode_barang = fields.Char(string='Kode Barang', readonly=True)
    nama_barang = fields.Char(string='Nama Barang', readonly=True)
    jumlah = fields.Float(string='Jumlah', readonly=True)
    satuan = fields.Char(string='Satuan', readonly=True)
    nilai = fields.Float(string='Nilai', readonly=True)
    currency = fields.Char(string='Currency', readonly=True)
    warehouse = fields.Char(string='Warehouse', readonly=True)
    
    # --- New Fields for Tabs ---
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    sisa_saldo_ids = fields.One2many('stock.quant', compute='_compute_sisa_saldo', string='Sisa Saldo Lines')
    consume_production_ids = fields.One2many('stock.move.line', compute='_compute_consume_production', string='Consume Production Lines')
    outgoing_ids = fields.One2many('stock.move.line', compute='_compute_outgoing', string='Outgoing Lines')

    def _compute_sisa_saldo(self):
        for line in self:
            # Finds current stock for the product in internal locations
            line.sisa_saldo_ids = self.env['stock.quant'].search([
                ('product_id', '=', line.product_id.id),
                ('quantity', '>', 0),
                ('location_id.usage', '=', 'internal')
            ])

    def _compute_consume_production(self):
        for line in self:
            # Finds moves where the product was sent to a production location
            line.consume_production_ids = self.env['stock.move.line'].search([
                ('product_id', '=', line.product_id.id),
                ('location_dest_id.usage', '=', 'production'),
                ('state', '=', 'done')
            ])

    def _compute_outgoing(self):
        for line in self:
            # Finds moves related to outgoing shipments
            line.outgoing_ids = self.env['stock.move.line'].search([
                ('product_id', '=', line.product_id.id),
                ('picking_id.picking_type_id.code', '=', 'outgoing'),
                ('state', '=', 'done')
            ])

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW %s AS (
            SELECT
                -- --- Add ROW_NUMBER() to generate the sequence ---
                ROW_NUMBER() OVER (ORDER BY sp.date_done, sp.name) as sequence,
                sml.id,
                p.id as product_id,
                doc.code as jenis_dok,
                bc.no_dok,
                bc.tgl_dok,
                sp.name as no_penerimaan,
                sp.date_done AS tgl_penerimaan,
                rp.name AS pengirim,
                pt.default_code as kode_barang,
                COALESCE(pt.name->>'en_US', pt.name->>'id_ID', pt.name->>0) as nama_barang,
                sml.qty_done as jumlah,
                COALESCE(uom.name->>'en_US', uom.name->>'id_ID', uom.name->>0) AS satuan,
                (sml.qty_done * sm.price_unit) AS nilai,
                cur.name AS currency,
                wh.code AS warehouse
            FROM
                stock_move_line sml
                JOIN stock_move sm ON sml.move_id = sm.id
                JOIN stock_picking sp ON sml.picking_id = sp.id
                LEFT JOIN purchase_order_line pol ON sm.purchase_line_id = pol.id
                LEFT JOIN purchase_order po ON pol.order_id = po.id
                LEFT JOIN res_currency cur ON po.currency_id = cur.id
                JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                JOIN product_product p ON sml.product_id = p.id
                JOIN product_template pt ON p.product_tmpl_id = pt.id
                JOIN uom_uom uom ON sml.product_uom_id = uom.id
                LEFT JOIN res_partner rp ON sp.partner_id = rp.id
                LEFT JOIN djbc_docs bc ON sp.djbc_docs_id = bc.id
                LEFT JOIN djbc_doctype doc ON bc.jenis_dok = doc.id
                LEFT JOIN stock_warehouse wh ON sp.picking_type_id = wh.in_type_id
            WHERE
                spt.code = 'incoming'
                AND sp.djbc_docs_id IS NOT NULL
                AND sp.state = 'done'
        )""" % (self._table,))