# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class mrp_repair(models.Model):
    _inherit = "mrp.repair.line"

    warranty = fields.Selection(
        [("iw", "IW"), ("oow", "OOW"), ("bad", "BAD")], "Garantía", required=True
    )
    type = fields.Selection(
        [("add", "Add"), ("remove", "Remove")], "Type", required=True, default="add"
    )

    @api.onchange("warranty")
    def onchange_warranty(self):
        for line in self:
            ASUS = 33
            SAT = 66
            DESECHADOS = 4
            PROD = 7
            if line.warranty == "iw":
                line.location_id = self.env["stock.location"].browse(ASUS)
            elif line.warranty == "oow":
                line.location_id = self.env["stock.location"].browse(SAT)
            elif line.warranty == "bad":
                line.location_id = self.env["stock.location"].browse(PROD)
                line.location_dest_id = self.env["stock.location"].browse(DESECHADOS)
