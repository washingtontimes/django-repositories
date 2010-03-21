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
    
    def create_remote(self, name, description='', homepage=''):
        """
        Create a remote repository on a separate service
        """
        raise NotImplementedError
    
    def add_remote(self, name, url, branch=None):
        """
        Add a remote repository
        """
        raise NotImplementedError
    
    def update_remote(self, name, branch=None):
        """
        Update a remote repository.
        """
        raise NotImplementedError
    
    def list_directory(self, path, revision=None, branch=None):
        """
        List the files directory in the repository
        
        Optionally can specify a revision or branch from which to show the directory.
        """
        raise NotImplementedError
    
    def get_file(self, path, revision=None, branch=None):
        """
        Get the contents from a file
        
        Optionally can specify a revision or branch from which to retrieve the contents
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
