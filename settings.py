from os import environ


SESSION_CONFIGS = [
    dict(
        name='HMCvsHHC',
        app_sequence=['Introduction', 'task1', 'chatHHC', 'chatHMC', 
                      'task2', 'chatHHC_2r', 'chatHMC_backup', 'survey', 'payment_info'], 
        num_demo_participants=100,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.5, doc=""
)

PARTICIPANT_FIELDS = ["wait_page_arrival", "avatar", "nickname", "taskType", "partnership", "partnerLabel"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='Room_A',
        display_name='Room A',
        participant_label_file='_rooms/econ101.txt',
        use_secure_urls=True,
    ),
    dict(
        name='Room_B', 
        display_name='Room B (no participant labels)',
    ),
    dict(
        name='Room_C', 
        display_name='Room C (no participant labels)',
    ),
    dict(
        name='Room_D', 
        display_name='Room D (no participant labels)',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Welcome to this experiment.
"""


SECRET_KEY = '{{ secret_key }}'

INSTALLED_APPS = ['otree']
