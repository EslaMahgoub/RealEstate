from odoo import api, fields, models, _

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence, name"
    
    name = fields.Char(string="Title", required=True)
    active = fields.Boolean(default=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order Types")
    
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         'The Name of a property type must be unique.'),
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)