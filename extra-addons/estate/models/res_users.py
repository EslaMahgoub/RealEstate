from odoo import api, fields, models


class User(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many("estate.property", 'salesman_id', domain="[('active', '=', True), ('state', 'in', ['new', 'offer_received'])]")