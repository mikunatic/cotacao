from odoo import fields, models, api, _

class Cotacao(models.Model):
    _name = 'cotacao'

    partner_id = fields.Many2one('res.partner', string="Cliente")
    partner_street = fields.Char(related='partner_id.street', string="Rua")
    partner_zip = fields.Char(related='partner_id.zip', string="Código Postal")
    partner_city = fields.Char(related='partner_id.city', string="Cidade")
    partner_route_id = fields.Many2one(related='partner_id.route_id')
    data_vencimento = fields.Date("Data de Vencimento")

    desejado_id = fields.Many2one('product.product')#, domain="[('id','not in',prod_cot_id)]"
    qnt_desejado = fields.Float(related='desejado_id.qty_available', string="Em estoque")
    quantidade_a_levar = fields.Float("Quantidade À Levar")
    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produto_cotado_rel", string="Produtos Cotados",
                                        options={'no_open': True, 'no_create': True, 'no_create_edit': True}, readonly=True)
    prod_cot_id = fields.One2many('produtos.cotados', 'cotacao_id',options={'no_open': True, 'no_create': True, 'no_create_edit': True})

    def carregaproduto(self):
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
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
    #     }
    @api.onchange("desejado_id")
    def domain_desejado_id(self):
        # for rec in self:
        #     pattern = '\d'
        #     string = ''
        #     result = re.findall(pattern, str(rec.id))
        #     print(result)
        #     for num in result:
        #         string += num
        #     prod_cot = self.env['produtos.cotados'].search([('cotacao_id', '=', int(string))])
        #     print(prod_cot)
        #     array = []
        #     for prod in prod_cot:
        #         array.append(prod.product_id.id)
        #     print(array)
        #     if rec.desejado_id:
        #         return {'domain': {'desejado_id': [('id', 'not in', array)]}}
        #     else:
        #         return {'domain': {'desejado_id': []}}
        for rec in self.prod_cot_id:
            print(rec)

