from odoo import models, fields, api, tools

class DjbcActivityLog(models.Model):
    _name = 'djbc.activity.log'
    _description = 'DJBC Activity Logs In Out'
    _auto = False
    _order = 'time desc'

    time = fields.Datetime(string="Time", readonly=True)
    resource_name = fields.Char(string="Resource Name", readonly=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)
    user_id = fields.Many2one('res.users', string="User", readonly=True)
    no_in_out = fields.Char(string="No Incoming/Outgoing", readonly=True)
    date_in_out = fields.Date(string="Date In/Out", readonly=True)
    dok_bc = fields.Char(string="Dok BC", readonly=True)
    no_pendaftaran = fields.Char(string="No Pendaftaran", readonly=True)
    tgl_pendaftaran = fields.Date(string="Tgl Pendaftaran", readonly=True)

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    sp.id as id,
                    sp.date_done as time,
                    CONCAT(sp.name, ': ', sl_origin.name, '->', sl_dest.name) as resource_name,
                    sp.state as status,
                    sp.write_uid as user_id,
                    sp.name as no_in_out,
                    CAST(sp.date_done AS DATE) as date_in_out,
                    doc_type.code as dok_bc,
                    docs.no_dok as no_pendaftaran,
                    docs.tgl_dok as tgl_pendaftaran
                FROM
                    stock_picking sp
                    LEFT JOIN res_users ru ON sp.write_uid = ru.id
                    LEFT JOIN stock_location sl_origin ON sp.location_id = sl_origin.id
                    LEFT JOIN stock_location sl_dest ON sp.location_dest_id = sl_dest.id
                    LEFT JOIN djbc_docs docs ON sp.djbc_docs_id = docs.id
                    LEFT JOIN djbc_doctype doc_type ON docs.jenis_dok = doc_type.id
                WHERE
                    sp.state = 'done'
            )
        """ % (self._table,))