import os
from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.template.loader import get_template

from repositories import settings

class Command(BaseCommand):
    help = "Generate an auth.wsgi script given the path to the project"
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("This command requires the path to the project as a parameter.")
        
        tmpl = get_template('repositories/auth.wsgi')
        ctxt_dict = {'project_root': args[0]}
        ctxt = Context(ctxt_dict)
        print tmpl.render(ctxt)
