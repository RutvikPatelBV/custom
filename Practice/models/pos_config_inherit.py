# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # pos.config fields
    pos_location_ids = fields.Many2many('practice.pos.config.location', config_parameter='practice.pos_location_ids', readonly=False)
