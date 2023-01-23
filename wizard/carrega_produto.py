from odoo import fields, models, api


class CarregaProduto(models.TransientModel):
    _name = 'carrega.produto'

    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    type = fields.Selection(related="desejado_id.type", string="Tipo de Produto")
    barcode = fields.Char(related="desejado_id.barcode", string="Código de Barras")
    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_rel", string="Produtos Cotados", readonly=True)

    alternativo = fields.Many2one(comodel_name='product.product', relation='cotacaov_rel', readonly=True)
    type_alt = fields.Selection(related="alternativo.type", string="Tipo de Produto")
    barcode_alt = fields.Char(related="alternativo.barcode", string="Código de Barras")

    acessorio_ids = fields.Many2many(related='desejado_id.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('id','not in',produtos_cotados)]")

    # def cotar_acessorio(self):
    #     prods = []
    #     for acess in self.produtos_cotados.ids:
    #         prods.append(acess)
    #     prods.append(self.acessorio)
    #     ctx = dict()
    #     ctx.update({
    #         'default_partner_id': self.partner_id.id,
    #         'default_data_vencimento': self.data_vencimento,
    #         'default_produtos_cotados': prods
    #     })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'cotacao',
    #         'views': [[self.env.ref("cotacao.cotacao_form_view").id, 'form']],
    #         'context': ctx,
    #         'target': 'new'
    #     }
    # def nao_cotar_acessorio(self):
    #     prods = []
    #     for acess in self.produtos_cotados.ids:
    #         prods.append(acess)
    #     ctx = dict()
    #     ctx.update({
    #         'default_partner_id': self.partner_id.id,
    #         'default_data_vencimento': self.data_vencimento,
    #         'default_produtos_cotados': prods
    #     })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'cotacao',
    #         'views': [[self.env.ref("cotacao.cotacao_form_view").id, 'form']],
    #         'context': ctx,
    #         'target': 'new'
    #     }
    def cotar(self):
        prods = []
        prods.append(self.desejado_id.id)
        for cotado in self.produtos_cotados.ids:
            prods.append(cotado)
        for acess in self.acessorio.ids:
            prods.append(acess)
        for alt in self.alternativo.ids:
            prods.append(alt)
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