import os, shutil
import settings

class BaseVCS(object):
    def __init__(self, name, anonymous_access, template=None):
        """
        A base class to handle Version Control System functions
        
        name = name of the repository
        anonymous_access = Is it public?
        template = The name of the template to use
        """
        self.public = anonymous_access
        self.name = name
        self.template = template
        self.config = self.get_config()
        self._update_path() # Sets self.path and url
    
    def _update_path(self):
        """
        Determine where the repository is. It is called in __init__ and sets 
        self.path and self.url
        """
        if self.public:
            self.path = os.path.abspath(os.path.join(self.config['public_path'], self.name))
            self.url = "%s%s/" % (self.config['public_url'], self.name)
        else:
            self.path = os.path.abspath(os.path.join(self.config['private_path'], self.name))
            self.url = "%s%s/" % (self.config['private_url'], self.name)
    
    
    def get_config(self):
        """
        Search the configuration for the correct record
        """
        name = self.__class__.__name__.replace('Repository','')
        for value in settings.VCS_CONFIG.values():
            if value['name'] == name:
                return value
        raise Exception("The configuration for %s is missing." % name)
    
    def exists(self):
        """
        Does the repository exist on the file system?
        """
        return os.path.exists(self.path)
    
    def create(self):
        """
        Create a new repository
        """
        NotImplementedError
    
    def make_public(self):
        """
        Move a repository from private to public
        """
        dest = os.path.abspath(os.path.join(self.config['public_path'], self.name))
        source = self.path
        shutil.move(source, dest)
        self.public = True
        self._update_path()
    
    def make_private(self):
        """
        Move a repository from public to private
        """
        source = self.path
        dest = os.path.abspath(os.path.join(self.config['private_path'], self.name))
        shutil.move(source, dest)
        self.public = False
        self._update_path()
    
    def delete(self):
        """
        Delete the source repository here
        """
        if self.exists():
            shutil.rmtree(self.path)
    
    def add_remote(self, name, url, branch=None):
        """
        Add a remote repository
        """
        raise NotImplementedError
    
    def list_directory(self, path):
        """
        List the files directory in the repository
        """
        raise NotImplementedError
    
    def get_absolute_url(self):
        """
        Return the absolute url
        """
        return self.url
    
    def get_current_revision(self):
        """
        Get the current revision of he repository
        """
        raise NotImplementedError
    
    def get_archive(self, revision=None, tag=None):
        """
        Get an archive of the current revision, or specific revision or tag
        """
        raise NotImplementedError


class SubversionRepository(BaseVCS):
    def create(self):
        """
        Create a source code repository
        """
        import subprocess
        if self.exists():
            return
        if not os.path.exists(self.config['public_path']):
            os.makedirs(self.config['public_path'])
        if not os.path.exists(self.config['private_path']):
            os.makedirs(self.config['private_path'])
        
        cmd = ["svnadmin","create", self.path]
        if self.config['config_dir']:
            cmd.extend(["--config-dir", self.config['config_dir']])
        subprocess.check_call(cmd)
        
        if self.template:
            template = os.path.join(os.path.dirname(__file__),'repo-templates',
                                        self.template)
            url = 'file://%s'%self.path
            cmd = ['svn', 'import', template, url, "-m", "\"Initial import.\""]
            if self.config['config_dir']:
                cmd.extend(["--config-dir", self.config['config_dir']])
            subprocess.check_call(cmd)
    
    def get_current_rev(self):
        from subprocess import PIPE, Popen
        import re
        rev = ''
        file_path = os.path.join(self.path, 'db/current')
        try:
            the_file = open(file_path, 'r')
            try:
                rev = the_file.readline().split()[0]
            finally:
                the_file.close()
        except IOError:
            pass
        return rev
    
    def list_directory(self, path):
        import pysvn, time
        client = pysvn.Client()
        dirlist = client.list("file://%s%s"%(self.path, path),
                              depth=pysvn.depth.immediates)
        results = []
        for item, locked in dirlist:
            if item.repos_path == path:
                continue
            results.append({
                'filename': os.path.basename(item.path),
                'dir_flag': (item.kind == pysvn.node_kind.dir),
                'size': item.size,
                'date': time.ctime(item.time),
                'author': item.last_author
            })
        return results


class BazaarRepository(BaseVCS):
    pass


class MercurialRepository(BaseVCS):
    pass


class GitRepository(BaseVCS):
    def __init__(self, name, anonymous_access, template=None):
        super(GitRepository, self).__init__(name, anonymous_access, template)
        if not self.name.endswith('.git'):
            self.name = "%s.git" % self.name
            self._update_path()
    
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