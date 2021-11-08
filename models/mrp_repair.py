# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class mrp_repair(models.Model):
    _inherit = "mrp.repair.line"

    warranty = fields.Selection(
        [("iw", "IW"), ("oow", "OOW"), ("na", "-")], "Garantía", default="na"
    )
