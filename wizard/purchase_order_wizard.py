# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createpurchaseorder_mrp(models.TransientModel):
    _name = "create.purchaseorder_mrp"
    _description = "Create Purchase Order"

    new_order_line_ids = fields.One2many(
        "getsale.mrpdata", "new_order_line_id", String="Order Line"
    )
    partner_id = fields.Many2one("res.partner", string="Vendor", required=True)
    date_order = fields.Datetime(
        string="Order Date", required=True, copy=False, default=fields.Datetime.now
    )

    @api.model
    def default_get(self, default_fields):
        res = super(createpurchaseorder_mrp, self).default_get(default_fields)
        data = self.env["mrp.repair"].browse(self._context.get("active_ids", []))
        update = []
        for record in data.operations:
            update.append(
                (
                    0,
                    0,
                    {
                        "product_id": record.product_id.id,
                        "product_uom": record.product_uom.id,
                        "order_id": record.repair_id.id,
                        "name": record.name,
                        "product_qty": record.product_uom_qty,
                        "price_unit": record.price_unit,
                        "product_subtotal": record.price_subtotal,
                        "warranty": record.warranty,
                    },
                )
            )
        res.update({"new_order_line_ids": update})
        return res

    @api.multi
    def action_create_purchase_order_mrp(self):
        self.ensure_one()
        res = self.env["purchase.order"].browse(self._context.get("id", []))
        value = []
        pricelist = self.partner_id.property_product_pricelist
        partner_pricelist = self.partner_id.property_product_pricelist
        mrp_repair_name = ""
        for data in self.new_order_line_ids:
            final_price = 00.0
            mrp_repair_name = data.order_id.name
            if partner_pricelist:
                product_context = dict(
                    self.env.context,
                    partner_id=self.partner_id.id,
                    date=self.date_order,
                    uom=data.product_uom.id,
                )

                final_price, rule_id = partner_pricelist.with_context(
                    product_context
                ).get_product_price_rule(
                    data.product_id, data.product_qty or 1.0, self.partner_id
                )
            # 				base_price, currency = self.with_context(product_context)._get_real_price_currency(data.product_id, rule_id, data.product_qty, data.product_uom, partner_pricelist)

            else:

                final_price = data.product_id.standard_price
        for data in self.new_order_line_ids:
            value.append(
                [
                    0,
                    0,
                    {
                        "product_id": data.product_id.id,
                        "name": data.name,
                        "product_qty": data.product_qty,
                        "order_id": data.order_id.id,
                        "product_uom": data.product_uom.id,
                        "taxes_id": ([(6, 0, data.product_id.supplier_taxes_id.ids)]),
                        "date_planned": datetime.today(),
                        "price_unit": final_price,
                    },
                ]
            )
        res.create(
            {
                "partner_id": self.partner_id.id,
                "date_order": self.date_order,
                "order_line": value,
                "origin": mrp_repair_name,
                "partner_ref": mrp_repair_name,
            }
        )
        return res


class Getmrprepairdata(models.TransientModel):
    _name = "getsale.mrpdata"
    _description = "Get MRP Repair Order Data"

    new_order_line_id = fields.Many2one("create.purchaseorder_mrp")
    seller_id = fields.Many2one("res.partner", compute="_compute_seller_id", readonly=False)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    name = fields.Char(string="Description")
    product_qty = fields.Float(string="Quantity", required=True)
    date_planned = fields.Date(string="Scheduled Date", default=datetime.today())
    product_uom = fields.Many2one("product.uom", string="Product Unit of Measure")
    order_id = fields.Many2one(
        "mrp.repair",
        string="Order Reference",
        required=True,
        ondelete="cascade",
        index=True,
        copy=False,
    )
    price_unit = fields.Float(
        string="Unit Price", required=True, digits=dp.get_precision("Product Price")
    )
    product_subtotal = fields.Float(string="Sub Total", compute="_compute_total")

    warranty = fields.Selection(
        [("iw", "IW"), ("oow", "OOW"), ("na", "-")], "Garantía", default="na"
    )
    
    @api.depends("product_qty", "price_unit")
    def _compute_total(self):
        for record in self:
            record.product_subtotal = record.product_qty * record.price_unit

    @api.depends("product_id")
    def _compute_seller_id(self):
        for rec in self:
            print(f"""
                seller ids -> {rec.product_id.seller_ids}
            """)