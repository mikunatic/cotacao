from odoo import fields, models,_


class Cotacao(models.TransientModel):
    _name = 'cotacao'

    partner_id = fields.Many2one('res.partner', string="Cliente")
    partner_street = fields.Char(related='partner_id.street', string="Rua")
    partner_zip = fields.Char(related='partner_id.zip', string="Código Postal")
    partner_city = fields.Char(related='partner_id.city', string="Cidade")
    partner_route_id = fields.Many2one(related='partner_id.route_id')
    data_vencimento = fields.Date("Data de Vencimento")

    desejado_id = fields.Many2one('product.product', domain="[('id','not in',produtos_cotados)]")
    qnt_desejado = fields.Float(related='desejado_id.qty_available', string="Em estoque")

    produtos_cotados = fields.Many2many(comodel_name='product.product', relation="produto_cotado_rel", string="Produtos Cotados",
                                        options={'no_open': True, 'no_create': True, 'no_create_edit': True}, readonly=True)

    def carregaproduto(self):
        ctx = dict()
        prods = []
        for produ in self.produtos_cotados.ids:
            prods.append(produ)
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_data_vencimento': self.data_vencimento,
            'default_desejado_id':self.desejado_id.id,
            'default_produtos_cotados':self.produtos_cotados.ids,
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
    def cria_cotacao_reg(self):
        reg = {
            'partner_id': self.partner_id.id,
            'data_vencimento':self.data_vencimento,
            'produtos_cotados':self.produtos_cotados.ids,
        }
        self.env['cotacao.reg'].create(reg)
        cr_criado = self.env['cotacao.reg'].search([],order='id desc')
        return {
            "type": "ir.actions.act_window",
            "name": _("Registro de Cotação"),
            "res_model": "cotacao.reg",
            "domain": [("id", "=", cr_criado[0].id)],
            "view_mode": "tree,form",
            "context": self.env.context
        }
