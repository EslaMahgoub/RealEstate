from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"
    
    
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'),
                   ('south', 'South'), 
                   ('east', 'East'), 
                   ('west', 'West')],
        )
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status', required=True, copy=False,selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ], default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Type', help="Type of the property.")
    tag_ids = fields.Many2many('estate.property.tag', string='Tags', help="Tags of the property.")
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False, help="Buyer of the property.")
    salesman_id = fields.Many2one('res.users', string='Salesman', help="Salesman of the property.", default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', help="Offers of the property.")
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    best_price = fields.Float(compute='_compute_best_price', store=True)
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The Expected Price of a property should be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The Selling Price of a property should be greater than or equal 0.')
    ]
    
    @api.ondelete(at_uninstall=False) 
    def _unlink_except_state_new_canceled(self):
        for record in self:
            if not record.state in ["new", "canceled"]:
                raise ValidationError("Cannot delete a property unless the state is 'new' or 'canceled' ")
                
                
            
    
    @api.constrains('expected_price', 'selling_price')
    def check_selling_price(self):
        """
        Raises a validation error if selling price is lower than 90% of expected price.
        """
        for record in self:
            if record.selling_price and not float_is_zero(record.expected_price, 2):
                if float_compare(record.selling_price, 0.9 * record.expected_price, 2) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
                
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
                
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.update({
                'garden_area': 10,
                'garden_orientation': "north"
                })
        else:
            self.update({
                'garden_area': 0,
                'garden_orientation': ""
            })
            return {'warning': {
                'title': _("Warning"),
                'message': ('No Garden in this property!')}}
                
    def action_set_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(_('Canceled property cannot be sold.'))
            else:
                record.state = "sold"
        return True
            
    def action_set_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_('Sold property cannot be canceled.'))
            else:
                record.state = "canceled"
        return True
            
            