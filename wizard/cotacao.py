from odoo import fields, models,api


class Cotacao(models.TransientModel):
    _name = 'cotacao'

    partner_id = fields.Many2one('res.partner', string="Cliente")
    partner_street = fields.Char(related='partner_id.street', string="Rua")
    partner_zip = fields.Char(related='partner_id.zip', string="Código Postal")
    partner_city = fields.Char(related='partner_id.city', string="Cidade")
    partner_route_id = fields.Many2one(related='partner_id.route_id')
    data_vencimento = fields.Date("Data de Vencimento")

    desejado_id = fields.Many2one('product.product', domain="[('id','not in',produtos_cotados)]")
    qnt_desejado = fields.Float(related='desejado_id.qty_available', string="Em estoque")

    alternativo_ids = fields.Many2many(related='desejado_id.optional_product_ids')
    alternativo = fields.Many2one('product.product', domain="[('product_tmpl_id','in',alternativo_ids)]")

    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produto_cotado_rel", string="Produtos Cotados")
    gambiarra = fields.Boolean("Gambiarra", compute='gambiarra')

#FAZER CONTEXT
    # def cotar_acessorio(self):
    #     ctx = dict()
    #     ctx.update({
    #         'default_partner_id': self.partner_id.id,
    #         'default_data_vencimento': self.data_vencimento,
    #         'default_desejado_id': self.desejado_id.id,
    #         'default_alternativo': self.alternativo.ids,
    #         'default_produtos_cotados': self.produtos_cotados.ids
    #     })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'carrega.produto',
    #         'views': [[self.env.ref("cotacao.carrega_produto_form_view").id, 'form']],
    #         'context': ctx,
    #         'target': 'new'
    #     }
    def carregaproduto(self):
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
            'default_desejado_id':self.desejado_id.id,
            'default_alternativo':self.alternativo.ids,
            'default_produtos_cotados':self.produtos_cotados.ids
        })
        return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'carrega.produto',
        'views': [[self.env.ref("cotacao.carrega_produto_form_view").id, 'form']],
        'context': ctx,
        'target': 'new'
        }
    def gambiarra(self):
        for produto in self.produtos_cotados.ids:
            if produto.qty_available > 0:
                self.bode_expiatorio = True
            elif produto.qty_available < 1:
                self.bode_expiatorio = False
    def cria_cotacao_reg(self):
        reg = {
            'partner_id': self.partner_id.id,
            'data_vencimento':self.data_vencimento,
            'produtos_cotados':self.produtos_cotados.ids,
        }
        self.env['cotacao.reg'].create(reg)