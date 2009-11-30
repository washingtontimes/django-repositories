import os
from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.template.loader import get_template

from repositories import settings

class Command(BaseCommand):
    help = "Generate an auth.wsgi script given the path to the project"
    def handle(self, *args, **options):
        ctxt_dict = {}
        if len(args) == 1:
            ctxt_dict['project_root'] = args[0]
        else:
            path = ''
            for item in args:
                key, val = item.split('=')
                ctxt_dict[key] = val
        
        tmpl = get_template('repositories/auth.wsgi')
        ctxt_dict.update(options)
        ctxt = Context(ctxt_dict)
        print tmpl.render(ctxt)
