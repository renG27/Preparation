# -*- coding: utf-8 -*-
from odoo import models

class MutasiXlsx(models.AbstractModel):
    _name = 'report.djbc_mutasi_gb.mutasi_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Laporan Mutasi XLSX'

    def generate_xlsx_report(self, workbook, data, objects):
        docs = self.env['djbc.mutasi_gb'].search([])
        
        form_data = data.get('form', {})
        date_start = form_data.get('date_start')
        date_end = form_data.get('date_end')
        kategori = form_data.get('kategori', 'Semua Kategori')

        sheet = workbook.add_worksheet('Laporan Mutasi')

        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        cell_format = workbook.add_format({'border': 1})
        
        sheet.merge_range('A1:M2', 'Laporan Mutasi', title_format)
        sheet.write('A4', 'Periode:')
        sheet.write('B4', f'{date_start} s/d {date_end}')
        sheet.write('A5', 'Kategori:')
        sheet.write('B5', kategori)
        
        # --- Updated Headers ---
        headers = [
            'No', 'Kode Barang', 'Nama Barang', 'Saldo Awal', 'Pemasukan',
            'Pengeluaran', 'Penyesuaian', 'Stock Opname', 'Saldo Akhir', 
            'Selisih', 'Satuan', 'Keterangan', 'Warehouse'
        ]
        for col, header in enumerate(headers):
            sheet.write(6, col, header, header_format)

        # --- Updated Data Writing ---
        row = 7
        for doc in docs:
            sheet.write(row, 0, doc.sequence, cell_format)
            sheet.write(row, 1, doc.kode_barang, cell_format)
            sheet.write(row, 2, doc.nama_barang, cell_format)
            sheet.write(row, 3, doc.saldo_awal, cell_format)
            sheet.write(row, 4, doc.pemasukan, cell_format)
            sheet.write(row, 5, doc.pengeluaran, cell_format)
            sheet.write(row, 6, doc.penyesuaian, cell_format)
            sheet.write(row, 7, doc.stock_opname, cell_format)
            sheet.write(row, 8, doc.saldo_akhir, cell_format)
            sheet.write(row, 9, doc.selisih, cell_format)
            sheet.write(row, 10, doc.satuan, cell_format)
            sheet.write(row, 11, doc.keterangan, cell_format)
            sheet.write(row, 12, doc.warehouse, cell_format)
            row += 1
            
        # Adjust column widths
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:M', 12)