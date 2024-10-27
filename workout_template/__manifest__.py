# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    'name': 'Workout Template',
    'version': '14.0.1.0.0',
    'category': 'Gym Management',
    'license': 'LGPL-3',
    'summary': 'This module is used for scheduling the Workout of the Member',
    'description': """This module is used for scheduling the Workout of the Member
        Workout Template
		Personal trainer workout plan template
		Fitness program template
		Exercise chart template
		Fitness plan template
		Exercise plan template exercise plan template
		Workout templates for personal trainers
		Workout template
		Workout plan template
		Workout schedule template
		Workout journal template
		Personal training program design templates
		Fitness calendar template
		Fitness schedule template
		Best workout log template
		Best workout template
		GYM workout template
		Personal training workout template
		Team workout template
		Workout plan template download
		Workout template app		
		""",
    
    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.",
  
    # Dependencies
    'depends': ['gym'],
    
    # Data
    'data': [
        'security/project_template_security.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/project_task_view.xml',
        'views/menuitem_hide.xml',
        'wizard/workout_schedule_view.xml',
    ],
    'demo': [
        'demo/workout_plan_demo_2.xml',
    ],
    
    # Odoo App Store Specific
    'images': ['static/description/Workout-Template-Banner.png'],
    
    # Technical
    'installable': True,
    'price': 99,
    'currency': 'EUR',
    'post_init_hook': '_post_init_hook',
}
