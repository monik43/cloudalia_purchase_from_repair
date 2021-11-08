# -*- coding: utf-8 -*-

{
    'name' : "Cloudalia Educacion Purchase from MRP Repair Order",
    'version' : "11.0.0.1",
    'author' : "Cloudalia Educacion",
    'summary': 'This apps helps to Covert Purchase order from MRP Repair Order',
    'description' : """
        Convert Purchase from MRP Repair Order
        Convert Purchases from MRP Repair Order
        Convert Purchase order from MRP Repair Order
        Convert Purchases order from MRP Repair Order

        create Purchase from MRP Repair Order
        create Purchases from MRP Repair Order
        create Purchase order from MRP Repair Order
        create Purchases order from MRP Repair Order


        Add Purchase from MRP Repair Order
        Add Purchases from MRP Repair Order
        ADD Purchase order from MRP Repair Order
        ADD Purchases order from MRP Repair Order

     """,
    'category' : "Purchases",
    'website'  : "https://www.cloudaliaeducacion.com",
    'depends'  : [ 'base','mrp_repair','purchase'],
    'data'     : [
                'wizard/purchase_order_wizard_view.xml',
                'views/inherit_mrp_order_view.xml',
            ],      
    'test' :  [ ],
    'css'  :  [ ],
    'demo' :  [ ],
    'installable' : True,
    'application' :  False,
    "images":['static/description/Banner.png'],
}
