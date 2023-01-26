from odoo import fields, models


class CarregaAlternativo(models.TransientModel):
    _name = 'carrega.alternativo'

    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_altern_rel",string="Produtos Cotados")
    variante = fields.Many2one('product.product', string="Produto", readonly=True)
    alternativo_ids = fields.Many2many(related='produtos_cotados.alternative_product_ids', relation='alt_prod')
    alternativo = fields.Many2one('product.product',domain="[('product_tmpl_id','in',alternativo_ids),('id','!=',desejado_id),('id','!=',variante)]")
