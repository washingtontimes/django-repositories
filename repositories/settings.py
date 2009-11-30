import os
from django.conf import settings

BIN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'bin'))

REPO_EXPORT_DIR = getattr(settings, 'REPO_EXPORT_DIR', 'exports')

default_base_repo_path = os.path.join(os.path.dirname(__file__), 'repositories')
BASE_REPO_PATH = getattr(settings, 'REPO_BASE_REPO_PATH', default_base_repo_path)

DEFAULT_VCS_CONFIG = {
    1:{
        'name':'Subversion',
        'command': 'svn',
        'public_path': os.path.join(BASE_REPO_PATH, 'svn', 'public') + "/",
        'private_path': os.path.join(BASE_REPO_PATH, 'svn', 'private') + "/",
        'public_url': '/svn/public/',
        'private_url': '/svn/private/',
        'config_dir': None,
    },
    2:{
        'name': 'Bazaar',
        'command': 'bzr',
        'public_path': os.path.join(BASE_REPO_PATH, 'bzr', 'public') + "/",
        'private_path': os.path.join(BASE_REPO_PATH, 'bzr', 'private') + "/",
        'public_url': '/bzr/public/',
        'private_url': '/bzr/private/',
    },
    3:{
        'name': 'Git',
        'command': 'git',
        'public_path': os.path.join(BASE_REPO_PATH, 'git', 'public') + "/",
        'private_path': os.path.join(BASE_REPO_PATH, 'git', 'private') + "/",
        'public_url': '/git/public/',
        'private_url': '/git/private/',
    },
    4:{
        'name': 'Mercurial',
        'command': 'hg',
        'public_path': os.path.join(BASE_REPO_PATH, 'hg', 'public') + "/",
        'private_path': os.path.join(BASE_REPO_PATH, 'hg', 'private') + "/",
        'public_url': '/hg/public/',
        'private_url': '/hg/private/',
    },
}

VCS_CONFIG = getattr(settings, 'REPO_VCS_CONFIG', DEFAULT_VCS_CONFIG)

DEFAULT_SVN_CONFIG_DIR = None
SVN_CONFIG_DIR = getattr(settings, 'REPO_SVN_CONFIG_DIR', DEFAULT_SVN_CONFIG_DIR)

def get_repo_template_choices():
    """
    Get a list of folders that contain the templates for first import.
    """
    rtmpls=os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), 'repo-templates')))
    return [(item,item) for item in rtmpls if item[0] != '.']

DEFAULT_METADATA_KEYS = ['Version',]
METADATA_KEYS = getattr(settings, 'REPO_METADATA_KEYS', DEFAULT_METADATA_KEYS)
try:
    VERSION_KEY = [key for key in METADATA_KEYS if key.lower() == 'version'][0]
except IndexError:
    VERSION_KEY = 'Version'
    METADATA_KEYS.append(VERSION_KEY)
METADATA_CHOICES = [(key, key) for key in METADATA_KEYS]

DEFAULT_URL_PATTERN = r'^/\w+/\w+/(?P<repo_name>\w+)/'
URL_PATTERN = getattr(settings, 'REPO_URL_PATTERN', DEFAULT_URL_PATTERN)

DEFAULT_WSGI_AUTH_SCRIPT = os.path.join(os.path.dirname(__file__),'bin','auth.wsgi')
WSGI_AUTH_SCRIPT = getattr(settings, 'REPO_WSGI_AUTH_SCRIPT', DEFAULT_WSGI_AUTH_SCRIPT)

WSGI_SCRIPT = getattr(settings, 'WSGI_SCRIPT', '')