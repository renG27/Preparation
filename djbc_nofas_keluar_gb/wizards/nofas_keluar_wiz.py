from odoo import models, fields, api

class DJBCNofasKeluargbWizard(models.TransientModel):
    _name = "djbc.nofas.keluar.gb.wizard"
    _description = "Wizard Laporan Pengeluaran"

    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)
    # --- Add this new field ---
    tipe_dokumen_id = fields.Many2one('djbc.doctype', string='Tipe Dokumen')

    def call_djbc_nofas_keluar_gb(self):
        self.ensure_one()
        
        # --- Build domain dynamically ---
        domain = [
            ('tgl_dok', '>=', self.date_start),
            ('tgl_dok', '<=', self.date_end)
        ]
        if self.tipe_dokumen_id:
            domain.append(('jenis_dok', '=', self.tipe_dokumen_id.code))
        
        return {
            'name': 'Laporan Pengeluaran',
            'type': 'ir.actions.act_window',
            'res_model': 'djbc.nofas_keluar_gb',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    def generate_laporan_xls(self):
        self.ensure_one()
        data = {
            'model': 'djbc.nofas.keluar.gb.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('djbc_nofas_keluar_gb.nofas_keluar_xlsx').report_action(self, data=data)

    @api.onchange('date_start', 'date_end')
    def onchange_date(self):
        res = {}
        if self.date_start and self.date_end and self.date_start > self.date_end:
            res = {'warning': {
                'title': ('Warning'),
                'message': ('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        return res