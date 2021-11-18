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
            ASUS_ID = 33
            SAT_ID = 66
            if line.warranty == "iw":
                line.location_id = self.env["stock.location"].browse(ASUS_ID)
            elif line.warranty == "oow":
                line.location_id = self.env["stock.location"].browse(SAT_ID)
            elif line.warranty == "bad":
                line.location_id = self.env["stock.location"].browse(4)
