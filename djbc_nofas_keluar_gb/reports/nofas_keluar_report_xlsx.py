# -*- coding: utf-8 -*-
from odoo import models

class NofasKeluarXlsx(models.AbstractModel):
    _name = 'report.djbc_nofas_keluar_gb.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Laporan Pengeluaran XLSX'

    def generate_xlsx_report(self, workbook, data, objects):
        # Get data from the wizard
        form_data = data.get('form', {})
        date_start = form_data.get('date_start')
        date_end = form_data.get('date_end')

        # --- Get the document type from the wizard data ---
        tipe_dokumen_id = form_data.get('tipe_dokumen_id')

        # --- Build the search domain dynamically ---
        domain = [
            ('tgl_dok', '>=', date_start),
            ('tgl_dok', '<=', date_end),
        ]
        if tipe_dokumen_id:
            doc_type = self.env['djbc.doctype'].browse(tipe_dokumen_id[0])
            domain.append(('jenis_dok', '=', doc_type.code))

        # --- Search for records using the new domain ---
        docs = self.env['djbc.nofas_keluar_gb'].search(domain)

        sheet = workbook.add_worksheet('Laporan Pengeluaran')

        # Cell formats
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        cell_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({'border': 1, 'num_format': 'dd/mm/yyyy'})

        # Report Header
        sheet.merge_range('A1:O2', 'Laporan Pengeluaran Barang', title_format)
        sheet.write('A4', 'Periode:')
        sheet.write('B4', f'{date_start} s/d {date_end}')

        # Table Headers
        headers = [
            'No', 'Jenis Dok', 'No Aju', 'Tgl Aju', 'No Daftar', 'Tgl Daftar', 
            'No Pengeluaran', 'Tgl Pengeluaran', 'No B/L', 'Tgl B/L', 
            'No Container', 'Penerima', 'Kode Barang', 'Nama Barang', 
            'Jumlah', 'Satuan', 'Nilai', 'Currency', 'Warehouse'
        ]
        for col, header in enumerate(headers):
            sheet.write(6, col, header, header_format)

        # Table Data
        row = 7
        for doc in docs:
            sheet.write(row, 0, doc.jenis_dok, cell_format)
            sheet.write(row, 1, doc.no_aju, cell_format)
            sheet.write(row, 2, doc.tgl_aju, date_format)
            sheet.write(row, 3, doc.no_dok, cell_format)
            sheet.write(row, 4, doc.tgl_dok, date_format)
            sheet.write(row, 5, doc.no_pengeluaran.name if doc.no_pengeluaran else '', cell_format)
            sheet.write(row, 6, doc.tgl_pengeluaran, date_format) # Assuming datetime, format if needed
            sheet.write(row, 7, doc.no_bl, cell_format)
            sheet.write(row, 8, doc.tgl_bl, date_format)
            sheet.write(row, 9, doc.no_cont, cell_format)
            sheet.write(row, 10, doc.penerima, cell_format)
            sheet.write(row, 11, doc.kode_barang, cell_format)
            sheet.write(row, 12, doc.nama_barang, cell_format)
            sheet.write(row, 13, doc.jumlah, cell_format)
            sheet.write(row, 14, doc.satuan, cell_format)
            sheet.write(row, 15, doc.nilai, cell_format)
            sheet.write(row, 16, doc.currency, cell_format)
            sheet.write(row, 17, doc.warehouse, cell_format)
            row += 1

        # Adjust column widths
        sheet.set_column('A:A', 12)
        sheet.set_column('B:E', 15)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:J', 15)
        sheet.set_column('K:L', 25)
        sheet.set_column('M:M', 35)
        sheet.set_column('N:R', 12)