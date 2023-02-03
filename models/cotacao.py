from odoo import fields, models, _, api
from odoo.exceptions import UserError
import re

class Cotacao(models.Model):
    _name = 'cotacao'

    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    cotacoes = fields.One2many(related='partner_id.cotacoes', string="Cotações anteriores")
    partner_street = fields.Char(related='partner_id.street', string="Rua")
    partner_zip = fields.Char(related='partner_id.zip', string="Código Postal")
    partner_city = fields.Char(related='partner_id.city', string="Cidade")
    partner_route_id = fields.Many2one(related='partner_id.route_id')
    data_vencimento = fields.Date("Data de Vencimento", default=fields.Date.today)

    desejado_id = fields.Many2one('product.product')
    qnt_desejado = fields.Float(related='desejado_id.qty_available', string="Em estoque")
    quantidade_a_levar = fields.Float("Quantidade À Levar")
    prod_cot_id = fields.One2many('produtos.cotados', 'cotacao_id', readonly=True, string="Produtos Cotados")
    int = fields.Integer()
    xml_id = fields.Integer(compute="pega_id")

    def carregaproduto(self):
        for rec in self:
            if rec.quantidade_a_levar > 0:
                ctx = dict()
                ctx.update({
                    'default_partner_id': self.partner_id.id,
                    'default_desejado_id': self.desejado_id.id,
                    'default_quantidade_a_levar': self.quantidade_a_levar
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
            elif rec.quantidade_a_levar == 0:
                raise UserError(_("Impossível cotar produto com quantidade igual à zero! \nSelecione uma quantidade."))
    def cria_pre_pedido(self):
            ctx = dict()
            for rec in self:
                rec.int = 10
                pattern = '\d'
                string = ''
                result = re.findall(pattern, str(rec.id))
                for num in result:
                        string += num
                vals_list = {
                    'cotacao':int(string),
                    'partner_id': self.partner_id.id,
                    'validity_date': self.data_vencimento,
                }
                quote = self.env['sale.order'].create(vals_list)
                for prods in self.prod_cot_id:
                    name = prods.name + ' ' + '(' + prods.product_template_attribute_value_ids.name + ')'
                    if prods.pre_pedido == True:
                        vals_lines = ({
                            'order_line': [(0, 0, {'product_id': prods.product_id.id,
                                                   'product_template_id': prods.product_id.product_tmpl_id,
                                                   'name': name,
                                                   'product_uom_qty': prods.quantidade_a_levar,
                                                    })]
                        })
                        quote.write(vals_lines)
                return {
                    'type': "ir.actions.act_window",
                    'view_type': "form",
                    'view_mode': "form",
                    'res_id': quote.id,
                    'res_model': "sale.order",
                    'views': [[self.env.ref("sale.view_order_form").id, 'form']],
                    'target': 'current',
                    'context': ctx
                }
    def abre_pre_pedido(self):
        for rec in self:
            ctx = dict()
            pattern = '\d'
            string = ''
            result = re.findall(pattern, str(rec.id))
            for num in result:
                string += num
            pp = self.env['sale.order'].search([('cotacao.id', '=', int(string))],order='id asc')  # pesquisar sale order q tem o id da cotacao atual no campo cotacao, depois retornar no domain
            return {
                "type": "ir.actions.act_window",
                "name": _(""),
                "res_model": "sale.order",
                "domain": [("id", "=", pp.id)],
                "view_mode": "tree,form",
                "context": self.env.context
            }
            # return {
            #     'type': "ir.actions.act_window",
            #     'view_type': "form",
            #     'view_mode': "form",
            #     'res_id': pp.id,
            #     'res_model': "sale.order",
            #     'views': [[self.env.ref("sale.view_order_form").id, 'form']],
            #     'target': 'current',
            #     'context': ctx
            # }
    def soma_duplicata(self):
        for rec in self:
            pattern = '\d+$' # regex q busca qualquer dígito
            var_id = 0 # variavel para armazenar o id da cotação atual
            var_id = re.findall(pattern, str(rec.id)) # dando o valor do id para a variavel var_id
            for produto in rec.prod_cot_id:
                #primeiro testar se tem proximo no array no for, fazer contador pra saber em qual index eu to, e comparar com o valor do index + 1 e fazer teste se o index + 1 existe
                for prox_produto in rec.prod_cot_id:
                    if produto.cotacao_id == prox_produto.cotacao_id and produto.product_id == prox_produto.product_id:
                        produto.quantidade_a_levar = produto.quantidade_a_levar + prox_produto.quantidade_a_levar
                        prox_produto
    def pega_id(self):
        for rec in self:
            pattern = '\d+$' # regex q busca qualquer dígito
            var_id = re.findall(pattern, str(rec.id))
            integerfication = int(var_id[0])
            rec.xml_id = integerfication
            cotacoes = self.env['cotacao'].search([])