from odoo import fields, models, api


class CarregaProduto(models.TransientModel):
    _name = 'carrega.produto'

    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    qnt_desejado = fields.Float(related='desejado_id.qty_available', string="Em estoque", store=True)
    quantidade_a_levar = fields.Float("Quantidade À Levar")
    type = fields.Selection(related="desejado_id.type", string="Tipo de Produto")
    barcode = fields.Char(related="desejado_id.barcode", string="Código de Barras")
    img = fields.Image(related="desejado_id.image_1920")
    partner_id = fields.Many2one('res.partner')

    acessorio_ids = fields.Many2many(related='desejado_id.accessory_product_ids')

    def cotar_acessorio(self):
        if self.quantidade_a_levar <= self.qnt_desejado:
            produto_desejado = {
                'product_id': self.desejado_id.id,
                'cotacao_id': self.env.context.get("active_id"),
                'quantidade_a_levar': self.quantidade_a_levar,
                'pre_pedido': True
            }
            self.env['produtos.cotados'].create(produto_desejado)

            acessorio = []
            for acess in self.acessorio_ids:
                if acess.qty_available > 0:
                    acessorio.append(acess.id)
            ctx = dict()
            ctx.update({
                'default_partner_id': self.partner_id.id,
                'default_desejado_id': self.desejado_id.id,
                'default_id_cotacao': self.env.context.get("active_id"),
                'default_acessorio': acessorio
            })
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'carrega.acessorio',
                'views': [[self.env.ref("cotacao.carrega_acessorio_form_view").id, 'form']],
                'context': ctx,
                'target': 'new'
            }
        elif self.quantidade_a_levar > self.qnt_desejado:
            produto_desejado = {
                'product_id': self.desejado_id.id,
                'cotacao_id': self.env.context.get("active_id"),
                'quantidade_a_levar': self.quantidade_a_levar,
                'pre_pedido': False
            }
            self.env['produtos.cotados'].create(produto_desejado)
            produto_desejado_maximo = { # vai cotar o máximo possível da quantidade do produto desejado
                'product_id': self.desejado_id.id,
                'cotacao_id': self.env.context.get("active_id"),
                'quantidade_a_levar': self.desejado_id.qty_available,
                'pre_pedido': True
            }
            self.env['produtos.cotados'].create(produto_desejado_maximo)
            ctx = dict()
            ctx.update({
                'default_partner_id': self.partner_id.id,
                'default_desejado_id': self.desejado_id.id,
                'default_id_cotacao': self.env.context.get("active_id"),
            })
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'carrega.variante',
                'views': [[self.env.ref("cotacao.carrega_variante_form_view").id, 'form']],
                'context': ctx,
                'target': 'new'
            }
    def naocotar(self):
        self.env['cotacao'].browse(self.env.context.get("active_id")).write({
            'desejado_id': False,
            'quantidade_a_levar': False
        })
        return