# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcCategs(models.Model):
    _name = 'djbc.categs'
    _description = 'DJBC Categories'
    _rec_name = 'name'

    name = fields.Char(string='DJBC Category', required=True)
    product_ids = fields.One2many('product.template', 'djbc_category_id', string='Products')
    product_count = fields.Integer(string='Product Count', compute='_compute_product_count')

    def _compute_product_count(self):
        for categ in self:
            categ.product_count = len(categ.product_ids)

    def action_view_products(self):
        return {
            'name': 'Products',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('djbc_category_id', '=', self.id)],
            'context': {'default_djbc_category_id': self.id}
        }