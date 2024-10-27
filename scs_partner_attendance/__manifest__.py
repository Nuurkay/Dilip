# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    "name": "SCS Partner Attendance",
    "version": "14.0.1.0.0",
    "license": "LGPL-3",
    "category": "Extra Tools",
    "summary": "SCS Partner Attendance allows to track attendance of partner and their check in and check out timings.",
    'description': """SCS Partner Attendance allows to track attendance of partner and their check in and check out timings.
        SCS Partner Attendance
		scs partner attendance system
		scs partner attendance software by odoo apps
		scs partner attendance by odoo apps
		partner attendance
		manage partner attendance
		manage partner attendance by report
		""",
    
    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
  
    # Dependencies
    "depends": ["contacts"],
    
    # Data
    "data": [
        "security/ir.model.access.csv",
        "views/partner_attendance_view.xml",
        "views/res_partner_view.xml",
        "wizard/attendance_summary_view.xml",
        "report/attendance_report.xml",
        "report/attendance_report_view.xml",
    ],
    
    # Odoo App Store Specific
    'images': ['static/description/Partner-Attendance-Banner.png'],
    
    # Technical
    "installable": True,
    "price": 20,
    "currency": "EUR",
}
