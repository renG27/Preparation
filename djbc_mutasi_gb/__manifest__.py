# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Mutasi GB',
    'version': '16.0.1.0.0',
    'summary': 'DJBC Laporan Mutasi GB',
    'description': 'DJBC Laporan Mutasi Berdasarkan Tanggal Penerimaan',
    'category': 'Extra Tools',
    'author': 'DPS-2025',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc_gb', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/mutasi.xml',
	    'reports/report.xml',
        'wizards/mutasi_wiz.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}