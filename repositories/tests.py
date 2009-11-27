import unittest, os
from projectmgr.models import SourceRepository
import settings
PUBLIC_REPO_DIR = settings.VCS_CONFIG[1]['public_path']
PRIVATE_REPO_DIR = settings.VCS_CONFIG[1]['private_path']

class SourceRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        src_repo = SourceRepository(name="public-repo", vc_system=1, anonymous_access=True)
        src_repo.save()
        src_repo = SourceRepository(name="private-repo", vc_system=1, anonymous_access=False)
        src_repo.save()
    
    def tearDown(self):
        objs = SourceRepository.objects.all()
        for obj in objs:
            obj.delete()
    
    def testNewPublicRepo(self):
        """
        Creating a new SourceRepository object should create a new repository
        """
        src_repo = SourceRepository.objects.get(name="public-repo")
        self.assertEquals(src_repo.repo_path, os.path.abspath(os.path.join(PUBLIC_REPO_DIR, 'public-repo')))
        self.assertTrue(os.path.exists(src_repo.repo_path))
    
    def testNewPrivateRepo(self):
        """
        Creating a new SourceRepository object should create a new repository
        """
        src_repo = SourceRepository.objects.get(name="private-repo")
        self.assertEquals(src_repo.repo_path, os.path.abspath(os.path.join(PRIVATE_REPO_DIR, 'private-repo')))
        self.assertTrue(os.path.exists(src_repo.repo_path))
    
    def testMovePrivateToPublic(self):
        """
        Switching the anonymous_access flag should change the location of the 
        repository
        """
        src_repo = SourceRepository.objects.get(name="private-repo")
        src_repo.anonymous_access = True
        src_repo.save()
        self.assertEquals(src_repo.repo_path, os.path.abspath(os.path.join(PUBLIC_REPO_DIR, 'private-repo')))
        self.assertTrue(os.path.exists(src_repo.repo_path))
    
    def testMovePrivateToPublic(self):
        """
        Switching the anonymous_access flag should change the location of the 
        repository
        """
        src_repo = SourceRepository.objects.get(name="public-repo")
        src_repo.anonymous_access = False
        src_repo.save()
        self.assertEquals(src_repo.repo_path, os.path.abspath(os.path.join(PRIVATE_REPO_DIR, 'public-repo')))
        self.assertTrue(os.path.exists(src_repo.repo_path))
    
    def testDeletePublicRemovesRepo(self):
        """
        Deleting the repository should remove the repository
        """
        src_repo = SourceRepository.objects.get(anonymous_access=True)
        repo_path = src_repo.repo_path
        src_repo.delete()
        self.assertFalse(os.path.exists(repo_path))
    
    def testDeletePrivateRemovesRepo(self):
        """
        Deleting the repository should remove the repository
        """
        src_repo = SourceRepository.objects.get(anonymous_access=False)
        repo_path = src_repo.repo_path
        src_repo.delete()
        self.assertFalse(os.path.exists(repo_path))

if __name__ == '__main__':
    unittest.main()
    