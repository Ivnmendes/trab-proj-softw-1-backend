import environ
import os
from django.conf.locale.pt_BR import formats as pt_BR_formats
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))

env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

MY_APPS = [
    'map',
    'medications'
]

INSTALLED_APPS = [
    'unfold',
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': env.db("DATABASE_URL") 
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_L10N = True

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    INSTALLED_APPS += ['storages']
    
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
    
    AWS_S3_REGION_NAME = 'us-east-2'
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "Gestão de Farmácias e Medicamentos",
    "SITE_HEADER": "Painel Administrativo",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Gestão de Saúde",
                "separator": True,
                "items": [
                    {
                        "title": "Medicamentos",
                        "icon": "medication", 
                        "link": reverse_lazy("admin:medications_medication_changelist"),
                    },
                    {
                        "title": "CIDs",
                        "icon": "monitor_heart", 
                        "link": reverse_lazy("admin:medications_cid_changelist"),
                    },
                    {
                        "title": "Documentos",
                        "icon": "description", 
                        "link": reverse_lazy("admin:medications_document_changelist"),
                    },
                ],
            },
            {
                "title": "Mapas e Localizações",
                "separator": True,
                "items": [
                    {
                        "title": "Farmácias",
                        "icon": "local_pharmacy", 
                        "link": reverse_lazy("admin:map_pharmacy_changelist"),
                    },
                    {
                        "title": "Pontos de Referência",
                        "icon": "location_on", 
                        "link": reverse_lazy("admin:map_landmark_changelist"),
                    },
                ],
            },
            {
                "title": "Administração",
                "separator": True,
                "items": [
                    {
                        "title": "Usuários",
                        "icon": "group", 
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Permissões",
                        "icon": "shield", 
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}