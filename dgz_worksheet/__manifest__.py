{
    'name': "dgz_worksheet",
    'version': '1.2',
    'summary': 'dgz_worksheet software',
    'depends': ['project','mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ws_security.xml',
        'views/worksheet.xml',
        'views/worksheet_tree.xml',
        'views/work_assign.xml',
    ],
    'assets': {
        'web.assets_backend': ['dgz_worksheet/static/src/js/navabar_menu.js',
                               'dgz_worksheet/static/src/css/my_style.css',
                               'dgz_worksheet/static/src/xml/navbarmenu.xml'],
    },
    'instalable': True,
    'application': True,
}
