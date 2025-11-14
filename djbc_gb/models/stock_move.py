# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcStockMove(models.Model):
    _inherit = 'stock.move'

    djbc_masuk_flag = fields.Boolean(string='DJBC Masuk')
    djbc_keluar = fields.Boolean(string='DJBC Keluar')