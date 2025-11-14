# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class DjbcDocs(models.Model):
    _name = 'djbc.docs'
    _description = 'DJBC Documents'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'no_dok'

    is_locked = fields.Boolean(string="Locked", default=False, copy=False)

    # Add this new field
    kode_dok_type = fields.Char(string='Kode Document Type', related='jenis_dok.code', readonly=True, store=True)

    no_dok = fields.Char(string='Nomor Dokumen BC', required=True, tracking=True)
    tgl_dok = fields.Date(string='Tanggal Dokumen BC', required=True, tracking=True)
    jenis_dok = fields.Many2one("djbc.doctype", string="Doc Type", required=True, tracking=True)
    no_aju = fields.Char(string="Nomor Pengajuan", tracking=True)
    tgl_aju = fields.Date(string="Tanggal Pengajuan")
    no_bl = fields.Char(string="Nomor B/L")
    tgl_bl = fields.Date(string="Tanggal B/L")
    jenis_bl = fields.Selection(
        string="Jenis B/L",
        selection=[("master", "Master"), ("house", "House")],
        default="house",
    )
    no_cont = fields.Char(string="Nomor Container")
    nm_cargoowner = fields.Many2one("res.partner", string="Nama Cargo Owner", tracking=True)
    npwpCargoOwner = fields.Char(string='NPWP Cargo Owner', related='nm_cargoowner.vat', readonly=False)
    no_doc_release = fields.Char(string='Doc Release No')
    date_doc_release = fields.Date(string='Doc Release Date')
    document_state = fields.Char(string='Document Status', tracking=True)
    id_platform = fields.Char(string='Id Platform', default='XXXXX')
    terminal = fields.Many2one("res.partner", string="Terminal", tracking=True)
    paid_thrud_date = fields.Date(string='Paid Date')
    proforma = fields.Char(string='Proforma')
    price = fields.Float(string="Price")
    proforma_date = fields.Date(string='Proforma Date')
    sent_sp2_date = fields.Date(string='Tgl Kirim SP2')
    status = fields.Char(string='Status')
    is_finished = fields.Boolean(string='Is Finished?', default=False, tracking=True)
    party = fields.Integer(string='Jumlah Container')
    keterangan = fields.Text(string="Keterangan")
    container_ids = fields.One2many("djbc.containers", "doc_id", string="Container List")
    request_date = fields.Date(string='Request DO Date')
    request_date_sp2 = fields.Date(string='Request SP2 Date')
    forwarder_name = fields.Many2one("res.partner", string="Nama FF/PPJK", tracking=True)
    id_ff_ppjk = fields.Char(string='NPWP FF/PPJK', related='forwarder_name.vat', readonly=False)
    shipping_name = fields.Many2one("res.partner", string="Shipping Name", tracking=True)
    price_do = fields.Float(string='Price DO')
    paid_date_do = fields.Date(string='Paid Date DO')
    status_do = fields.Char(string='Status DO', tracking=True)
    do_number = fields.Char(string='Nomor DO')
    do_date_number = fields.Date(string='Tgl DO')
    sent_do_date = fields.Date(string='Tgl Kirim DO')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['is_locked'] = True
        return super(DjbcDocs, self).create(vals_list)

    def write(self, vals):
        if 'is_locked' not in vals:
            vals['is_locked'] = True
        res = super(DjbcDocs, self).write(vals)
        return res

    def action_unlock(self):
        self.write({'is_locked': False})

    # (sisa method import Anda tetap di sini)
    def action_open_base_import(self):
        return {
            'name': 'Import Records',
            'type': 'ir.actions.act_window',
            'res_model': 'base_import.import',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_res_model': self._name}
        }
    def _import_enabled(self):
        return True