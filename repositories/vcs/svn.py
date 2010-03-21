import os
from base import BaseVCS

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
