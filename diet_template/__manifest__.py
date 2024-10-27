# See LICENSE file for full copyright and licensing details.

{
    # Module Info.
    'name': 'Diet Template',
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Gym Management',
    'summary': 'The Diet Plan Template Management System module is manage Diet Plan Designing and Scheduling.',
    'description': """The Diet Plan Template Management System module is manage Diet Plan Designing and Scheduling.
        Diet Template Management
		Diet Template
		Diet Plan Designing and Scheduling
		Diet app template 
		Diet plan template 
		Diet record template 
		Diet schedule template 
		Diet design template 
		Diet plan sheet template 
		Diet plan table template 
		Diet analysis template
		Diet diary template
		Diet food journal template
		Diet food log template
		Diet meal plan template
		Diet meal template
		Diet plan schedule template
		Diet planner template
		Diet planning template
		Diet website template
		Meals diet plan template
		Odoo Diet Template
		Odoo DietTemplate Management
		Diet Template Management System
		odoo diet plan template 
		Diet Template Management System in odoo
		Diet plan template tool
		""",
    
    # Author
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "website": "http://www.serpentcs.com",
    "maintainer": "Serpent Consulting Services Pvt. Ltd.", 
    
    # Dependencies
    'depends': ['gym'],
    
    # Data
    'data': [
        'security/ir.model.access.csv',
        'views/diet_view.xml',
        'views/project_view.xml',
        'views/project_task_view.xml',
        'views/menuitem_hide.xml',
        'views/sale_order_view.xml',
        'wizard/diet_schedule_view.xml',
    ],
    'demo': [
        'demo/diet_plan_demo.xml',
    ],
    
    # Odoo App Store Specific
    'images': ['static/description/gym2.jpg'],
    
    # Technical
    'installable': True,
    'sequence': 1,
    'price': 99,
    'currency': 'EUR',
}
