# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcStockPicking(models.Model):
    _inherit = 'stock.picking'

    djbc_docs_id = fields.Many2one('djbc.docs', string='DJBC Document')

    # --- ADD THESE NEW FIELDS ---
    jenis_dok_bc = fields.Char(
        string='Jenis Dokumen',
        related='djbc_docs_id.jenis_dok.code',
        readonly=True,
        store=True
    )
    tgl_dok_bc = fields.Date(
        string='Tanggal Dokumen',
        related='djbc_docs_id.tgl_dok',
        readonly=True,
        store=True
    )
    # --------------------------
    
    def _create_backorder(self):
        """
        This is the new method.
        It creates the backorder and then clears the djbc docs.
        """
        backorders = super()._create_backorder()
        if backorders:
            backorders.write({"djbc_docs_id": False})
        return backorders