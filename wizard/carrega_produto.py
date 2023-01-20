from odoo import fields, models, api


class CarregaProduto(models.TransientModel):
    _name = 'carrega.produto'

    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    type = fields.Selection(related="desejado_id.type", string="Tipo de Produto")
    barcode = fields.Char(related="desejado_id.barcode", string="Código de Barras")
    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_rel", string="Produtos Cotados", readonly=True)

    def cotar(self):
        prods = []
        for cotado in self.produtos_cotados.ids:
            prods.append(cotado)
        prods.append(self.desejado_id.id)
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento' : self.data_vencimento,
            'default_produtos_cotados': prods
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacao',
            'views': [[self.env.ref("cotacao.cotacao_form_view").id, 'form']],
            'context': ctx,
            'target': 'new'
        }
    def naocotar(self):
        prods = []
        for cotado in self.produtos_cotados.ids:
            prods.append(cotado)
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
            'default_produtos_cotados': prods
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacao',
            'views': [[self.env.ref("cotacao.cotacao_form_view").id, 'form']],
            'context': ctx,
            'target': 'new'
        }