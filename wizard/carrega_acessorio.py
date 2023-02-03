from odoo import fields, models,_
from odoo.exceptions import UserError


class CarregaAcessorio(models.TransientModel):
    _name = 'carrega.acessorio'

    partner_id = fields.Many2one('res.partner')
    desejado_id = fields.Many2one('product.product', string="Produto", readonly=True)
    preco_desejado_id = fields.Float(related='desejado_id.standard_price', string="Preço do Produto", readonly=True)
    acessorio_ids = fields.Many2many(related='desejado_id.accessory_product_ids')
    acessorio = fields.Many2many('product.product', domain="[('id','in',acessorio_ids),('qty_available','>',0)]")
    id_cotacao = fields.Integer()

    def cotar(self):
        for acess in self.acessorio:
            acessorio_cotar = ({
                'product_id': acess.id,
                'cotacao_id': self.id_cotacao,
                'quantidade_a_levar': acess.quantidade_a_levar,
                'pre_pedido': True
            })
            if acess.quantidade_a_levar <= acess.qty_available:
                self.env['produtos.cotados'].create(acessorio_cotar)
            elif acess.quantidade_a_levar > acess.qty_available:
                raise UserError(_("Impossível cotar quantidade maior que a quantidade em estoque"))
            acess.quantidade_a_levar = 0
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
        })
        self.env['cotacao'].browse(self.id_cotacao).write({
            'desejado_id': False,
            'quantidade_a_levar': False
        })
        return
    # def return_all_books(self):
    #     self.ensure_one()
    #     wizard = self.env['library.return.wizard']
    #     with Form(wizard) as return_form:
    #         return_form.borrower_id = self.partner_id.id
    #     record = return_form.save()
    #     record.books_returns()