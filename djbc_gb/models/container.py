# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcContainers(models.Model):
    _name = 'djbc.containers'
    _description = 'DJBC Containers'
    _rec_name = 'name'

    name = fields.Char(string='Container No', required=True)
    container_size = fields.Char(string='Size')
    container_type = fields.Char(string='Type')
    gate_pass = fields.Char(string='Gate Pass')
    doc_id = fields.Many2one("djbc.docs", string="DJBC Doc")