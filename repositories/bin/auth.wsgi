#!/usr/bin/env python
import os, sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT,"apps"))
sys.path.insert(0, os.path.join(PROJECT_ROOT,"lib"))
sys.path.insert(0, PROJECT_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.utils import importlib
from django.contrib.auth.models import User
from django import db


def check_password(environ, user, password):
    db.reset_queries() 
    try: 
        try: 
            user = User.objects.get(username=user, is_active=True)
        except User.DoesNotExist: 
            return None
            
        if user.check_password(password):
            return True
        else: 
            return False
    finally: 
        db.connection.close()


def groups_for_user(environ, user):
    import re
    from repoman import settings
    from repoman.models import SourceRepository
    groups = []
    db.reset_queries()
    try:
        try:
            user = User.objects.get(username=user, is_active=True)
        except User.DoesNotExist:
            return groups
        
        try:
            repo_name = re.match(settings.URL_PATTERN, environ['REQUEST_URI']).group('repo_name')
        except:
            return groups
        
        try:
            repo = SourceRepository.objects.get(name=repo_name)
            if repo.anonymous_access or repo.user_can_read(user):
                groups.append('read')
            if repo.user_can_write(user):
                groups.append('write')
        except SourceRepository.DoesNotExist:
            return groups
    finally:
        db.connection.close()
    return groups
