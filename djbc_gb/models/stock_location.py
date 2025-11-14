# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcStockLocation(models.Model):
    _inherit = 'stock.location'

    is_stock_location = fields.Boolean(string="Is a Stock Location?")