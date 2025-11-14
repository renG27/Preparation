# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcProductTemplate(models.Model):
    _inherit = 'product.template'

    hscode = fields.Many2one("djbc.hscode", string="HS Code")
    djbc_category_id = fields.Many2one("djbc.categs", string="DJBC Category")