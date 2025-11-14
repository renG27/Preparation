# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcDocType(models.Model):
    _name = 'djbc.doctype'
    _description = 'DJBC Document Type'
    _rec_name = 'code'

    code = fields.Char(string='Doc. Type', required=True)
    is_import_doc = fields.Boolean(string='Is an Import Document?', default=False)