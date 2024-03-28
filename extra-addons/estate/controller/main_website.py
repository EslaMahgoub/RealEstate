from odoo import http
from odoo.http import request


class EstateProperty(http.Controller):
    #type ="http", "json"
    #auth ="public", "users, "none"
    #sudo() => because no user has any access to the db so we need to add sudo
    @http.route('/estate_property_details', type="http", auth="public", website=True)
    def get_sale_orders(self, **kwargs):
        estate_property_details = request.env['estate.property'].sudo().search([])
        return request.render('estate.estate_property_details', {'estate_property_details': estate_property_details})
        
    @http.route("/new_property_request_submit", type="http", auth="public", website=True, csrf=True)
    def request_submit(self, **kwargs):
        vals = {
            "name": kwargs.get('st_name'),
            "expected_price": kwargs.get('st_expected_price'),
            "garden": True
        }
        estate_propety_id = request.env['estate.property'].sudo().create(vals)
        return request.render('estate.success', {'estate_propety_id': estate_propety_id})