# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for Property'
    _sql_constraints = [
        ('check_amount', 'CHECK(amount > 0)', 'The amount must be strictly positive')
    ]

    display_name = fields.Char(
        string='Name',
        compute='_compute_display_name'
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )
    seller_id = fields.Many2one(
        'res.partner',
        string='Seller',
        related='property_id.owner_id'
    )
    city_of_property = fields.Char(
        string='City',
        related='property_id.city'
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    amount = fields.Monetary('Amount')
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency'
    )
    offer_date = fields.Datetime(
        string='Date of Offer',
        default=fields.Date.context_today
    )
    validity_date = fields.Datetime(
        string='Validity Date',
        compute='_compute_validity_date',
        store=True,
    )
    offer_state_id = fields.Many2one(
        'estate.property.offer.state',
        string='State'
    )

    @api.depends('offer_date')
    def _compute_validity_date(self):
        for offer in self:
            if offer.offer_date:
                offer.validity_date = offer.offer_date + timedelta(days=30)


    def _compute_display_name(self):
        for record in self:
            if record.buyer_id and record.property_id:
                record.display_name = record.property_id.name + ' - ' + record.buyer_id.name
            else:
                record.display_name = 'SUPER OFFRE POUR' + ' - ' + record.property_id.name