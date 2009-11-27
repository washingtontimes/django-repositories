import os
from django.core.management.base import BaseCommand
from repositories import settings
from repositories.models import SourceRepository


class Command(BaseCommand):
    def handle(self, *args, **options):
        os.chdir(settings.REPO_EXPORT_DIR)
        for repo in SourceRepository.objects.filter(anonymous_access=True):
            if repo.get_vc_system_display() == 'Subversion':
                os.system('svn export file://%s/trunk %s' % (repo.repo_path, repo.name) )
                os.system('zip -r %s.zip %s' % (repo.name, repo.name) )
                os.system('tar -czvf  %s.tgz %s' % (repo.name, repo.name) )
                os.system('rm -rf %s' % repo.name)
            elif repo.get_vc_system_display() == 'Git':
                os.system('git clone file://%s %s' % (repo.repo_path, repo.name) )
                os.chdir(repo.name)
                os.system('git archive master --format=zip -o ../%s.zip' % repo.name)
                os.system('git archive master --format=tar  | gzip > ../%s.tgz' % repo.name)
                os.chdir('..')
                os.system('rm -rf %s' % repo.name)
