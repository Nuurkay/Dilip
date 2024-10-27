# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    "name": "GYM Management System",
    "version": "14.0.1.0.0",
    "category": "Gym Management",
    "license": "LGPL-3",
    "summary": "Master module to get whole Gym Management Package",
    "description": """This modules implements GYM management system with the following entities
		Member
		Trainer
		Operator,
        GYM Management System
		GYM Management
		GYM management system software
		GYM management system
		GYM management system project
		GYM management system odoo
		Odoo GYM Management System
		GYM Equipments
		GYM Management System with odoo
		GYM Management System in odoo
		GYM membership management software
		GYM launch management
		GYM management system website
		GYM membership management
		GYM membership management system
		GYM management system app
		GYM management system plan
		GYM management system project
		GYM management system tools
		GYM facility management system
		GYM management system roles
		GYM member management system
		Management system of gym
		GYM Workout Plans
		GYM Diet Plans
		Diet Plan Assignment of Gym Management
		Configure Day-wise Workout Tasks in gym management
		Odoo Gym
		Gym Odoo
		management
		Gym
		""",
    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
    
    # Dependencies
    "depends": [
        "workout_template",
        "diet_template",
        "trainer_booking",
        "gym_employee_attendance",
    ],
    
    # Odoo App Store Specific
    "images": ["static/description/gym.jpg"],
    "live_test_url": "https://www.youtube.com/watch?v=wjwHTyee3m8&list=PL4Wugt3LKrSSxMqCpwP5N64NSVzWxve79",
   
    # Technical
    "installable": True,
    "application": True,
    "price": 5,
    "currency": "EUR",
}
