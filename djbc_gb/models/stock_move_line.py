# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    sisa_qty = fields.Float(string='Sisa Qty')
    jumlah_kemasan = fields.Float(string="Jumlah Kemasan")
    satuan_kemasan = fields.Char(string="Satuan Kemasan")
    djbc_masuk_flag = fields.Boolean(related='move_id.djbc_masuk_flag', string='DJBC Masuk', store=True)
    djbc_keluar = fields.Boolean(related='move_id.djbc_keluar', string='DJBC Keluar', store=True)

    # --- NEW FIELDS FOR OUTGOING TAB ---
    djbc_docs_id = fields.Many2one(
        'djbc.docs', 
        string='DJBC Document',
        related='picking_id.djbc_docs_id', 
        store=True
    )
    jenis_dok_bc = fields.Char(
        string='Jns Dok BC',
        related='djbc_docs_id.jenis_dok.code', 
        store=True
    )
    no_dok_bc = fields.Char(
        string='No Dok BC',
        related='djbc_docs_id.no_dok', 
        store=True
    )
    tgl_dok_bc = fields.Date(
        string='Tgl Dok BC',
        related='djbc_docs_id.tgl_dok', 
        store=True
    )