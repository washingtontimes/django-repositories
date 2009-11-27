import os
from django.core.management.base import BaseCommand
from repositories import settings
from repositories.models import SourceRepository
from repositories.signals import repository_changed

class Command(BaseCommand):
    def handle(self, *args, **options):
        for repo in SourceRepository.objects.all():
            try:
                current_rev = repo._vcs.get_current_rev()
                if current_rev != repo.current_rev:
                    repo.previous_rev = repo.current_rev
                    repo.current_rev = current_rev
                    repo.save()
                    repository_changed.send(sender=repo, current_rev= current_rev, previous_rev=repo.previous_rev)
            except:
                # If there was an error, we'll move on.
                continue