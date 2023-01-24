from odoo import fields, models


class CarregaAlternativo(models.TransientModel):
    _name = 'carrega.alternativo'

    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    desejado_id = fields.Many2one('product.product', string="Produto")
    desejado_tmpl_id = fields.Many2one(related="desejado_id.product_tmpl_id")
    alternativo = fields.Many2one('product.product', domain="[('product_tmpl_id','=',desejado_tmpl_id),('id','!=',desejado_id)]")# domain="[('product_tmpl_id','in',alternativo_ids)]"
    qnt_desejado = fields.Float(related='alternativo.qty_available')
    #type = fields.Selection(related="alternativo.type", string="Tipo de Produto")
    ##barcode = fields.Char(related="alternativo.barcode", string="Código de Barras")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_alt_rel", string="Produtos Cotados")

    acessorio_ids = fields.Many2many(related='alternativo.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('id','not in',produtos_cotados)]")

    def cotar_alt(self):
        prods = []
        prods.append(self.desejado_id.id)
        prods.append(self.alternativo.id)
        for cotado in self.produtos_cotados.ids:
            prods.append(cotado)
        for acess in self.acessorio.ids:
            prods.append(acess)
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
    def nao_cotar_alt(self):
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
    def cotar_acessorio(self):
        ctx = dict()
        ctx.update({
            'default_partner_id':self.partner_id.id,
            'default_data_vencimento':self.data_vencimento,
            'default_produtos_cotados':self.produtos_cotados.ids,
            'default_desejado_id':self.desejado_id.id
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