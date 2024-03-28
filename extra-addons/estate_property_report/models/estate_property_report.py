from odoo import api, fields, models, _, tools

class EstatePropertyReport(models.Model):
    _name = "estate.property.report"
    _description = "Estate Property Report"
    _order = "id desc"
    _auto = False
    
    estate_name = fields.Char(string="Title", required=True)
    selling_price = fields.Float()
    
    partner_name = fields.Char("Partner Name")
    partner_email = fields.Char("Partner Email")
    partner_phone = fields.Char("Partner phone")
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
        create or replace view {} as (
        select estate.id as id,
        estate.selling_price as selling_price,
        estate.name as estate_name,
        partner.name as partner_name,
        partner.email as partner_email,
        partner.phone as partner_phone
        from estate_property as estate join res_partner as partner on
        estate.partner_id=partner.id)
        """.format(self._table))