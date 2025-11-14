{
    'name': 'DJBC Activity Log GB',
    'version': '16.0.1.0.0',
    'summary': 'Provides an activity log for incoming and outgoing warehouse operations GB',
    'category': 'Extra Tools',
    'author': 'DPS-2025',
    'website': '-',
    'depends': ['djbc_gb', 'stock', 'auditlog'],
    'data': [
        'security/ir.model.access.csv',
        'views/activity_log_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
}