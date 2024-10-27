# See LICENSE file for full copyright and licensing details.

{
    'name': 'Trainer Booking',
    'description': """
    This module is used for Trainer Booking in Gym
    Trainer Booking For a Session
    Can Create Training Session.
    Book Trainer for that Session.
    Can select Members who Attend the Session.
    Can select a Trainer for the Session.
    Can Book a Trainer based on duration.
    Trainer Booking is based on Trainer's Working Schedule.
    """,
    'summary': """
    Trainer Booking in Gym
    Trainer Booking For a Session
    Book a Trainer based on duration.
    Trainer Booking is based on Trainer's Working Schedule.
    """,
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'category': 'Gym Management',
    'depends': [
        'gym',
        'hr_holidays'
    ],
    'data': [
        'views/trainer_booking_view.xml',
        'views/hr_employee_view.xml',
        'views/partner_view.xml',
        'views/trainer_view.xml',
    ],
    'images': ['static/description/gym4.jpg'],
    'installable': True,
    'price': 49,
    'currency': 'EUR',
}
