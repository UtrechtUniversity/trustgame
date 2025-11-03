from os import environ

SESSION_CONFIGS = [
    dict(
        name='Trust_Game',
        num_demo_participants=300,
        app_sequence=['role_assignment', 'truster', 'trustee']
    )
]

ROOMS = [
    dict(
        name='ODISSEI',
        display_name='ODISSEI'
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1,
    participation_fee=0)

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'secret'

