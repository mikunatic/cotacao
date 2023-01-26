from odoo import fields, models


class CarregaAcessorio(models.TransientModel):
    _name = 'carrega.acessorio'

    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_aces_rel", string="Produtos Cotados", readonly=True)
    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    acessorio_ids = fields.Many2many(related='desejado_id.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('id','not in',produtos_cotados)]")

    def cotar(self):
        prods = []
        prods.append(self.desejado_id.id)
        for acessorio in self.acessorio.ids:
            prods.append(acessorio)
        for produtos in self.produtos_cotados.ids:
            prods.append(produtos)
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
            'default_produtos_cotados': prods,
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
