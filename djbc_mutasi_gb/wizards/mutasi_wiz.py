import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# --- TAMBAHKAN FUNGSI INI ---
def _get_default_category(self):
    # Fungsi ini akan membaca context yang dikirim dari menu
    return self.env.context.get('default_djbc_category_id', None)
# ---------------------------

class DJBCMutasiWizard(models.TransientModel):
    _name = 'djbc.mutasiwizardgb'

    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)
    
    # --- MODIFIKASI FIELD INI ---
    # Tambahkan default=_get_default_category
    djbc_category_id = fields.Many2one(
        comodel_name="djbc.categs", 
        string="DJBC Category",
        default=_get_default_category
    )
    # ---------------------------
    
    kategori = fields.Char(string="Kategori")
    
    def generate_laporan(self):
        self.ensure_one()
        cr = self.env.cr
        category_id = self.djbc_category_id.id if self.djbc_category_id else None
        cr.execute("select djbc_mutasi_gb(%s, %s, %s)", (self.date_start, self.date_end, category_id))
        
        return {
            'name': 'Laporan Mutasi',
            'type': 'ir.actions.act_window',
            'res_model': 'djbc.mutasi_gb',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def generate_laporan_xls(self):
        self.ensure_one()
        cr = self.env.cr
        category_id = self.djbc_category_id.id if self.djbc_category_id else None
        cr.execute("select djbc_mutasi_gb(%s, %s, %s)", (self.date_start, self.date_end, category_id))
        
        data = {
            'model': 'djbc.mutasiwizardgb',
            'form': self.read()[0]
        }
        
        return self.env.ref('djbc_mutasi_gb.mutasi_xlsx').report_action(self, data=data)

    @api.onchange('date_start', 'date_end')
    def onchange_date(self):
        res = {}
        if self.date_start and self.date_end and self.date_start > self.date_end:
            res = {'warning': {
                'title': ('Warning'),
                'message': ('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        if res:
            return res

    @api.onchange('djbc_category_id')
    def onchange_kategori(self):
        if self.djbc_category_id:
            self.kategori = self.djbc_category_id.name
        else:
            self.kategori = False
        return