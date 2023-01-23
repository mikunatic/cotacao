from odoo import api, models


class ProductExtension(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        name_split = name.split()
        array = []
        for palavra in name_split:
            array.append('|')
            array.append('|')
            array.append(('name', operator, palavra))
            array.append(('product_template_attribute_value_ids',operator,palavra))
            array.append(('fipe_ids',operator,palavra))
        if name:
            pesquisa = self.search(array)
            return pesquisa.name_get()
        return self.search([('name',operator,name)]+args, limit=limit).name_get()