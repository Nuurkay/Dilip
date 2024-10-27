# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    "name": "GYM Employee Attendance",
    "version": "14.0.1.0.0",
    "license": "LGPL-3",
    "category": "Gym Management",
    "summary": "GYM Employee Attendance allows to track attendance of trainer, member and their check in and check out timings.",
    'description': """GYM Employee Attendance allows to track attendance of trainer, member and their check in and check out timings.
        GYM Employee Attendance
		gym employee attendance system
		gym employee attendance software by odoo apps
		scs gym employee attendance by odoo apps
		gym attendance
		manage gym attendance
		manage gym attendance for trainer,member
		manage gym attendance by report
		track gym attendance of member and trainer software
		""",
		
	# Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
  
    # Dependencies
    "depends": ["gym", "hr_holidays", "scs_partner_attendance"],
    
    # Data
    "data": [
        "security/ir.model.access.csv",
        "security/attendance_security.xml",
        "views/gym_employee_attendance.xml",
        "views/gym_member_partner_view.xml",
        "views/hr_employee_view.xml",
        "wizard/employee_attendance_summary_view.xml",
        "wizard/member_attendance_summary_view.xml",
        "report/employee_attendance_report.xml",
        "report/employee_attendance_report_view.xml",
    ],
    
    # Odoo App Store Specific
    'images': ['static/description/GYM-Employee-Attendance-Banner.png'],
    
    # Technical
    "installable": True,
    "price": 49,
    "currency": "EUR",
}
