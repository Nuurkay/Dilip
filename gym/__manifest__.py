# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    'name': 'GYM Management',
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Gym Management',
    'summary': 'This module is used for Gym Management with Membership,'
    ' Trainer, and Equipment.',
    'description': """This module is used for Gym Management with Membership, Trainer, and Equipment.
        GYM Management
		GYM management software
		GYM management system
		GYM management project 
		GYM management odoo 
		Odoo GYM Management
		GYM Management with odoo
		GYM Management in odoo
		GYM membership management software
		GYM launch management
		GYM management system website
		GYM membership management
		GYM management app
		GYM management plan
		GYM management project
		GYM management tools
		GYM facility management 
		GYM management roles
		Odoo Gym
		Gym Odoo
		Management
		Gym
		""",
		
	# Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
  
    # Dependencies	
    'depends': [
        'sale_management',
        'hr',
        'crm',
        'project',
        'membership'
    ],
    
    # Data
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/member_sequence.xml',
        'data/membership_plan_sequence.xml',
        'data/equipment_demo.xml',
        'data/email_template.xml',
        'data/membership_scheduler.xml',
        'data/service_demo.xml',
        'data/exercise_for_demo.xml',
        'data/exercise_demo.xml',
        'data/mail_templates.xml',
        'views/menuitem_hide.xml',
        'views/product_template.xml',
        'views/membership_view.xml',
        'views/project_task_view.xml',
        'views/member_view.xml',
        'views/trainer_view.xml',
        'views/workout_view.xml',
        'views/company_view.xml',
        'views/gym_skills_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
        'demo/exercise_exercise_demo.xml',
        'demo/user_demo.xml',
        'demo/pedo_meter_demo.xml',
        'demo/food_demo.xml',
        'demo/membership_demo.xml'
    ],
    
    # Odoo App Store Specific
    'images': ['static/description/gym.jpg'],
    
     # Technical
    'application': False,
    'installable': True,
    'price': 199,
    'currency': 'EUR',
}
