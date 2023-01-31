from odoo import fields, models


class ProdutosCotados(models.Model):
    _name = 'produtos.cotados'
    _inherits = {"product.product": "product_id"}

    quantidade_a_levar = fields.Float("Quantidade à Levar")
    product_id = fields.Many2one('product.product')
    custo = fields.Float(related="product_id.standard_price")
    cotacao_id = fields.Many2one('cotacao')
    pre_pedido = fields.Boolean("Pré-Pedido")
    qty_available = fields.Float(related="product_id.qty_available")
