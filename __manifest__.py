{
    'name': 'Cotação',
    'category': 'Vendas',
    'summary': 'Cotação',
    'version': '1.0',
    'description': """Cadastro de Cotações""",
    'depends': ['product','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cotacao_view.xml',
        'wizard/carrega_produto_view.xml',
        'views/cotacao_reg_view.xml',
        'wizard/carrega_variante_view.xml',
        'wizard/carrega_acessorio_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
