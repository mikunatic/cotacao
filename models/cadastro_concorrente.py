from odoo import fields, models


class CadastroConcorrente(models.Model):
    _name = 'cadastro.concorrente'

    concorrente_id = fields.Char("Concorrente")
    product_id = fields.Many2one('product.product')
    product_price = fields.Float(related='product_id.lst_price', string="Preço Padrão")
    preco_concorrente = fields.Float('Preço de concorrente')