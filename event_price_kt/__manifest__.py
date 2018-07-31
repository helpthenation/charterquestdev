{
    "name": "Event Customization",
    "version": "1.0",
    "depends": ["base", "sale_management", "event_sale", "event", "event_price", "account", "website_event"],
    "author": "Kiran <kiran@strategicdimensions.co.za>",
    "category": "Custom",
    "description": "Adds a custom Pricing to OpenERP events",
    "data": [
        # 'views/pcexam_voucher_report.xml',
        # 'views/email_templates_data.xml',
        # 'security/ir.model.access.csv',
        "views/event_view_inh_kt.xml",
        "views/report_view.xml",
        "views/customer_view.xml",
        "views/event_discount_view.xml",
        "views/semister_view.xml",
        'wizard/pcexam_wizard_view.xml',
        # 'security/security.xml',
    ],
    "test": [],
    "installable": True,
    "active": False
}
