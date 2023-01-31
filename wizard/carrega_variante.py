from odoo import fields, models, api,_
from odoo.exceptions import UserError


class CarregaVariante(models.TransientModel):
    _name = 'carrega.variante'

    partner_id = fields.Many2one('res.partner')
    data_vencimento = fields.Date("Data de Vencimento")
    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    desejado_tmpl_id = fields.Many2one(related="desejado_id.product_tmpl_id")
    variante = fields.Many2one('product.product')
    qnt_variante = fields.Float(related='variante.qty_available', string="Quantidade em estoque")
    a_levar = fields.Float("À Levar (Por favor, selecionar quantidade igual ou menor à do estoque)", domain="[(a_levar,'>=',0),(a_levar,'<=',qnt_variante)]")
    qnt_desejado = fields.Float(related='variante.qty_available')
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produtos_cotados_var_rel", string="Produtos Cotados")
    id_cotacao = fields.Integer()

    acessorio_ids = fields.Many2many(related='variante.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('id','not in',produtos_cotados),('qty_available','>',0)]", relation="acess_do_var_rel")
    int = fields.Integer("int")
    filtro_alternativo = fields.Integer("filt")

    alternativo_ids = fields.Many2many(related="desejado_id.alternative_product_ids", relation="alternativo_da_variante_rel")
    alternativo = fields.Many2one("product.product")
    qnt_alternativo = fields.Float(related='alternativo.qty_available', string="Quantidade em estoque")

    acessorio_alt_ids = fields.Many2many(related='alternativo.accessory_product_ids', relation="acess_domain_alt_rel")
    acessorio_alt = fields.Many2many('product.product', domain="[('id','in',acessorio_alt_ids),('id','not in',produtos_cotados),('qty_available','>',0)]", relation="acess_do_alter_rel")

    def cotar_acessorio_variante(self):
        ctx = dict()
        if self.variante:
            if self.a_levar > self.qnt_variante:
                raise UserError(_('Quantidade desejada não pode ser maior que a quantidade em estoque!'))
        if self.alternativo:
            if self.a_levar > self.qnt_alternativo:
                raise UserError(_('Quantidade desejada não pode ser maior que a quantidade em estoque!'))
        if self.acessorio:
            for acessorio in self.acessorio.ids:
                acessorio_cotar = {
                    'product_id': acessorio,
                    'cotacao_id': self.id_cotacao,
                    'quantidade_a_levar': 1,
                    'pre_pedido': True
                }
                self.env['produtos.cotados'].create(acessorio_cotar)
        if self.acessorio_alt:
            for acessorio in self.acessorio_alt.ids:
                acessorio_cotar = {
                    'product_id': acessorio,
                    'cotacao_id': self.id_cotacao,
                    'quantidade_a_levar': 1,
                    'pre_pedido': True
                }
                self.env['produtos.cotados'].create(acessorio_cotar)
        if self.variante:
            variante = {
                'product_id': self.variante.id,
                'cotacao_id':self.id_cotacao,
                'quantidade_a_levar':self.a_levar,
                'pre_pedido': True
            }
            self.env['produtos.cotados'].create(variante)
        if self.alternativo:
            alternativo = {
                'product_id': self.alternativo.id,
                'cotacao_id': self.id_cotacao,
                'quantidade_a_levar': self.a_levar,
                'pre_pedido': True
            }
            self.env['produtos.cotados'].create(alternativo)
        return
    @api.onchange('desejado_id')
    def domain_variante(self):
        records = self.env['product.product'].search([('product_tmpl_id','=',self.desejado_tmpl_id.id),('id','!=',self.desejado_id.id),('qty_available','>',0),('id','not in',self.produtos_cotados.ids)])
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
    def concluir(self): # cotar
        ctx = dict()
        for acessorio in self.acessorio.ids:
            acessorio_cotar = {
                'product_id': acessorio,
                'cotacao_id': self.id_cotacao,
            }
            self.env['produtos.cotados'].create(acessorio_cotar)
        for acessorio in self.acessorio_alt.ids:
            acessorio_cotar = {
                'product_id': acessorio,
                'cotacao_id': self.id_cotacao,
            }
            self.env['produtos.cotados'].create(acessorio_cotar)
        self.env['produtos.cotados'].create(self.variante)
        self.env['produtos.cotados'].create(self.alternativo)
        self.env['produtos.cotados'].create(self.a_levar)
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
        })
        return
    @api.onchange('desejado_id')
    def domain_alt(self):
        domain = []
        search_alt = self.env['product.product'].search([('id','in',self.alternativo_ids.ids),('qty_available','>',0),('id','not in',self.produtos_cotados.ids)])
        for id in search_alt.ids:
            domain.append(id)
        print(domain)
        length = len(domain)
        if length == 0:
            self.filtro_alternativo = 1
        elif length > 0:
            self.filtro_alternativo = 2
        if self.desejado_id:
            return {"domain": {'alternativo': [('id', 'in', domain)]}}
        else:
            return {'domain': {'alternativo': []}}