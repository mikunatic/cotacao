from odoo import fields, models, api


class CarregaVariante(models.TransientModel):
    _name = 'carrega.variante'
#fazer campo de produto alternativo e acessório do alternativo
    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    desejado_tmpl_id = fields.Many2one(related="desejado_id.product_tmpl_id")
    variante = fields.Many2one('product.product', domain="[('product_tmpl_id','=',desejado_tmpl_id),('id','!=',desejado_id)]")# domain="[('product_tmpl_id','in',alternativo_ids)]"
    qnt_desejado = fields.Float(related='variante.qty_available')
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_var_rel", string="Produtos Cotados")

    acessorio_ids = fields.Many2many(related='variante.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('id','not in',produtos_cotados)]", relation="acess_do_var_rel")
    int = fields.Integer("chui")

    alternativo_ids = fields.Many2many(related="desejado_id.alternative_product_ids", relation="alternativo_da_variante_rel")
    alternativo = fields.Many2one("product.product", domain="[('id','in',alternativo_ids)]")

    acessorio_alt_ids = fields.Many2many(related='alternativo.accessory_product_ids', relation="acess_domain_alt_rel")
    acessorio_alt = fields.Many2many('product.product', domain="[('id','in',acessorio_alt_ids),('id','not in',produtos_cotados),('qty_available','>',0)]", relation="acess_do_alter_rel")

    def nao_cotar_variante(self):
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
    def cotar_acessorio_variante(self):
        ctx = dict()
        ctx.update({
            'default_partner_id':self.partner_id.id,
            'default_data_vencimento':self.data_vencimento,
            'default_produtos_cotados':self.produtos_cotados.ids,
            'default_desejado_id':self.desejado_id.id,
            'default_alternativo':self.variante.id
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'carrega.acessorio.alternativo',
            'views': [[self.env.ref("cotacao.carrega_acessorio_variante_form_view").id, 'form']],
            'context': ctx,
            'target': 'new'
        }
    @api.onchange('desejado_id')
    def domain_variante(self):
        records = self.env['product.product'].search([('product_tmpl_id','=',self.desejado_tmpl_id.id),('id','!=',self.desejado_id.id),('qty_available','>',0)])
        array = []
        for id in records.ids:
            array.append(id)
        length = len(array)
        if length == 0:
            self.int = 1
        elif length > 0:
            self.int = 2
        if self.desejado_id:
            return {"domain": {'variante': [('id', 'in', array)]}}
        else:
            return {'domain': {'variante': []}}
    def carrega_alternativo(self): # cotar
        ctx = dict()
        prods = []
        prods.append(self.desejado_id.id)
        prods.append(self.variante.id)
        prods.append(self.alternativo.id)
        for cotado in self.acessorio_alt.ids:
            prods.append(cotado)
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
            'default_produtos_cotados': prods,
            'default_desejado_id': self.desejado_id.id,
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