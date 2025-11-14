# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Pengeluaran GB',
    'version': '16.0.1.0.0',
    'summary': 'DJBC Laporan Pengeluaran Fasilitas TPB dan Non Fasilitas GB',
    'description': '...',
    'category': 'Extra Tools',
    'author': 'DPS-2025',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc_gb', 'stock_picking_invoice_link', 'report_xlsx'], # Add 'report_xlsx' here
    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml', # Add this line
        'wizards/nofas_keluar_wiz.xml',
        'views/nofas_keluar.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}