from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"
    
    name = fields.Char(string="Title", required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer()
    
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         'The Name of a property tag must be unique.'),
    ]