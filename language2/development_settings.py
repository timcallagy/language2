# -*- coding: utf-8 -*-
from .settings import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {
     'default': {
             'ENGINE': 'django.db.backends.postgresql_psycopg2', 
             'NAME': 'language2db',  
             'USER': 'muwawa',
             'PASSWORD': 'FMtf9whG',
             'HOST': '',  
             'PORT': '', 
         }
}
