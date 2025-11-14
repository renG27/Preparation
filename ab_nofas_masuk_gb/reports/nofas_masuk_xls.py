# -*- coding: utf-8 -*-
from odoo import models

class NofasMasukXlsx(models.AbstractModel):
    _name = 'report.ab_nofas_masuk_gb.nofas_masuk_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Laporan Pemasukan XLSX'

    def generate_xlsx_report(self, workbook, data, lines):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        # --- Get the document type from the wizard data ---
        tipe_dokumen_id = data['form'].get('tipe_dokumen_id')

        sheet = workbook.add_worksheet('Pemasukan')
        format1 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format2 = workbook.add_format({'font_size': 12, 'align': 'center'})
        sheet.merge_range('A1:N1', 'Laporan Pemasukan', format1)
        sheet.merge_range('A2:N2', f'Periode: {date_start} s.d. {date_end}', format1)

        headers = [
            'No', 'Jenis Dokumen', 'Nomer Pendaftaran', 'Tanggal Pendaftaran',
            'Nomer Penerimaan', 'Tanggal Penerimaan', 'Pengiriman Barang',
            'Kode Barang', 'Nama Barang', 'Jumlah', 'Satuan', 'Nilai',
            'Currency', 'Warehouse'
        ]
        for col, header in enumerate(headers):
            sheet.write(3, col, header, format1)

        # --- Build the search domain dynamically ---
        domain = [
            ('tgl_penerimaan', '>=', date_start),
            ('tgl_penerimaan', '<=', date_end),
        ]
        if tipe_dokumen_id:
            # The wizard passes the ID and name, so we get the ID from the list
            doc_type = self.env['djbc.doctype'].browse(tipe_dokumen_id[0])
            domain.append(('jenis_dok', '=', doc_type.code))

        # --- Search for records using the new domain ---
        report_lines = self.env['djbc.nofas_masuk_gb'].search(domain)

        no = 1
        row = 4
        for obj in report_lines:
            sheet.write(row, 0, no, format2)
            sheet.write(row, 1, obj.jenis_dok or '', format2)
            sheet.write(row, 2, obj.no_dok or '', format2)
            sheet.write(row, 3, str(obj.tgl_dok) if obj.tgl_dok else '', format2)
            sheet.write(row, 4, obj.no_penerimaan or '', format2)
            sheet.write(row, 5, str(obj.tgl_penerimaan) if obj.tgl_penerimaan else '', format2)
            sheet.write(row, 6, obj.pengirim or '', format2)
            sheet.write(row, 7, obj.kode_barang or '', format2)
            sheet.write(row, 8, obj.nama_barang or '', format2)
            sheet.write(row, 9, obj.jumlah, format2)
            sheet.write(row, 10, obj.satuan or '', format2)
            sheet.write(row, 11, obj.nilai, format2)
            sheet.write(row, 12, obj.currency or '', format2)
            sheet.write(row, 13, obj.warehouse or '', format2)

            no += 1
            row += 1