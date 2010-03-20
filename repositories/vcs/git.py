import os
from base import BaseVCS
from repositories import settings

class GitRepository(BaseVCS):
    def __init__(self, name, anonymous_access, template=None):
        super(GitRepository, self).__init__(name, anonymous_access, template)
        if not self.name.endswith('.git'):
            self.name = "%s.git" % self.name
            self._update_path()
    
    def create_remote(self, name, description='', homepage=''):
        from github2.client import Github
        github = Github(username=settings.GITHUB_USER, api_token=settings.GITHUB_API_TOKEN)
        new_repo = github.repo.create(name, description, homepage, public=True)
        commit_url = new_repo.url.replace('http://','git@') + '.git'
        return commit_url
    
    def add_remote(self, name, url, branch=None):
        import subprocess
        repo_path = self.path
        cmd = ["cd %s;git remote add %s %s" % (repo_path, name, url),]
        try:
            subprocess.check_call(cmd, shell=True)
        except:
            pass
        
    def remove_remote(self, name):
        import subprocess
        repo_path = self.path
        cmd = ["cd %s;git remote rm %s" % (repo_path, name),]
        try:
            subprocess.check_call(cmd, shell=True)
        except:
            pass
    
    def update_remote(self, name, branch=None):
        import subprocess
        repo_path = self.path
        the_branch = branch or "master"
        cmd = ["cd %s;git push %s %s" % (repo_path, name, branch)]
        try:
            subproc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = subproc.communicate()
        except:
            pass
    
    def create(self):
        import subprocess
        if self.exists():
            return
        if not os.path.exists(self.config['public_path']):
            os.makedirs(self.config['public_path'])
        if not os.path.exists(self.config['private_path']):
            os.makedirs(self.config['private_path'])
        repo_path = self.path
        os.mkdir(repo_path, 0744)
        cmd = ["cd %s;git --bare init;git --bare update-server-info" % repo_path,]
        subprocess.check_call(cmd, shell=True)
        cmd = ['%s file://%s/' % (os.path.join(settings.BIN_PATH, 'initialize_git_repo.sh'), repo_path)]
        subprocess.check_call(cmd, shell=True)
    
    def get_current_rev(self):
        from subprocess import PIPE, Popen
        cmd = ['cd %s;git show --pretty=format:"%%H" --quiet' % self.path,]
        return Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE).communicate()[0]
    
    def archive(self, revision=None, tag=None):
        """
        Execute git archive <HEAD or revision or tag> | gzip -c 
        """
        pass