import logging
from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)
class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            vals = {
                "partner_id": record.partner_id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                Command.create({
                    "name": f"{record.name} Invoice",
                    "quantity": "1",
                    "price_unit": 0.6 * record.selling_price + 100,
                })
            ],
            }
            self.env['account.move'].create(vals)
        return super().action_set_sold()
