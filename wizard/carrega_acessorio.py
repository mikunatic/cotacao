from odoo import fields, models


class CarregaAcessorio(models.TransientModel):
    _name = 'carrega.acessorio'

    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_aces_rel", string="Produtos Cotados", readonly=True)
    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    acessorio_ids = fields.Many2many(related='desejado_id.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('id','not in',produtos_cotados),('qty_available','>',0)]")
    id_cotacao = fields.Integer()

    def cotar(self):
        prods = []
        for acessorio in self.acessorio.ids:
            acessorio_cotar = {
                'product_id': acessorio,
                'cotacao_id': self.id_cotacao,
                'quantidade_a_levar': 1,
                'pre_pedido': True
            }
            self.env['produtos.cotados'].create(acessorio_cotar)
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
            'default_produtos_cotados': prods,
        })
        self.env['cotacao'].browse(self.id_cotacao).write({
            'desejado_id': False,
            'quantidade_a_levar': False
        })
        return

