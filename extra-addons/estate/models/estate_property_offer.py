from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"
    
    price = fields.Float(string="Price")
    active = fields.Boolean(default=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False, required=True, help="Buyer of the property.")
    state = fields.Selection(string='Status', readonly=True, copy=False, selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ])
    validity = fields.Float(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', default= lambda self: fields.Date().today())
    property_id_state = fields.Selection(string="Property Status", related='property_id.state')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Propety Type', help="Type of the property.", store=True)
    
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Price of a property offer must be greater than 0.'),
    ]
    
    @api.model
    def create(self, vals):
        property_obj = self.env['estate.property'].browse(vals['property_id'])
        existing_offers = property_obj.offer_ids.mapped('price')
        if any(offer_price >= vals['price'] for offer_price in existing_offers):
            raise ValidationError("The offer you are submitting is lower than or equal to an existing offer.")

        # Set the property state to 'offer_received' before creating the offer
        property_obj.state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals)
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
    
    def action_set_accepted(self):
        for record in self:
            record.state = "accepted"
            record.property_id.state = "sold"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
        return True
            
    def action_set_refused(self):
        for record in self:
            record.state = "refused"
        return True
    