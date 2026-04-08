{
    'name': 'Office Access Card',
    'version': '14.0.1.0.0',
    'summary': 'Gestión de tarjetas de acceso de oficina',
    'description': """
        Módulo para gestionar tarjetas de acceso de oficina.
        Permite registrar tarjetas, responsables, estados
        y enviar mensajes al chatter.
    """,
    'author': 'Tu Nombre o Empresa',
    'category': 'Administration',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/office_access_card_views.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': True,
}