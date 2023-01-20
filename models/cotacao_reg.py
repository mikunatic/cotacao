from odoo import fields, models


class CotacaoReg(models.Model):
    _name = 'cotacao.reg'

    partner_id = fields.Many2one('res.partner')
    partner_street = fields.Char(related='partner_id.street', string="Rua")
    partner_zip = fields.Char(related='partner_id.zip', string="Código Postal")
    partner_city = fields.Char(related='partner_id.city', string="Cidade")
    partner_route_id = fields.Many2one(related='partner_id.route_id')
    data_vencimento = fields.Date("Data de Vencimento")

    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produto_cotado_rel_reg",
                                        string="Produtos Cotados")