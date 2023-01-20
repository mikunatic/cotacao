from odoo import api, models


class ProductExtension(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            pesquisa = self.search(['|','|',('name',operator,name),('product_template_attribute_value_ids',operator,name),('fipe_ids',operator,name)])
            return pesquisa.name_get()
        return self.search([('name',operator,name)]+args, limit=limit).name_get()