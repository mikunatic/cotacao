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
    data_vencimento = fields.Date("Data de Vencimento")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_rel", string="Produtos Cotados", readonly=True)

    def cotar_acessorio(self):
        if self.quantidade_a_levar <= self.qnt_desejado:
            produto_desejado = {
                'product_id': self.desejado_id.id,
                'cotacao_id': self.env.context.get("active_id"),
                'quantidade_a_levar': self.quantidade_a_levar
            }
            self.env['produtos.cotados'].create(produto_desejado)
            ctx = dict()
            ctx.update({
                'default_partner_id':self.partner_id.id,
                'default_data_vencimento':self.data_vencimento,
                'default_desejado_id':self.desejado_id.id,
                'default_id_cotacao': self.env.context.get("active_id")
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
            prods = []
            for produto in self.produtos_cotados.ids:
                prods.append(produto)
            prods.append(self.desejado_id.id)
            produto_desejado = {
                'product_id': self.desejado_id.id,
                'cotacao_id': self.env.context.get("active_id"),
                'quantidade_a_levar': self.quantidade_a_levar
            }
            self.env['produtos.cotados'].create(produto_desejado)
            ctx = dict()
            ctx.update({
                'default_partner_id': self.partner_id.id,
                'default_data_vencimento': self.data_vencimento,
                'default_desejado_id': self.desejado_id.id,
                'default_id_cotacao': self.env.context.get("active_id")
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