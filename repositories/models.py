import shutil, os

from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings as global_settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

import settings, vcs

"""
Uses the types of version control systems configured through the 
``REPO_VCS_CONFIG`` setting to create a ``list`` of ``integer``, ``string`` 
``tuples``. It is used for :attr:`SourceRepository.vc_system` choices.
"""
VC_TYPE_CHOICES = [(key, value['name']) for key, value in settings.VCS_CONFIG.items()]

"""A dictionary that maps a version control name to the appropriate class defined in :mod:`projectmgr.vcs`\ ."""
VCS = {}
for key, value in settings.VCS_CONFIG.items():
    VCS[key] = getattr(vcs, value['name']+'Repository')


#: Bitwise permissions:
#: 
#: * 1 = Read
#: * 2 = Write
#: * 4 = Owner
PERM_CHOICES = (
    (1, "Read"),
    (3, "Read/Write"),
    (7, "Owner")
)


class SourceRepositoryManager(models.Manager):
    
    def get_for_user(self, user, permission=3):
        """
        Return a list of source repositories which the user has at least the
        given permission level
        
        :param user: The :class:`User` for which to find :class:`SourceRepository` instances.
        :type user: :class:`User`
        :param permission: The type of permission, one of :data:`repositories.models.PERM_CHOICES`\ . **Default:** 3 (read/write)
        :type permission: `integer`
        :returns: A :class:`QuerySet` of :class:`SourceRepository`
        :rtype: :class:`QuerySet`
        """
        project_ids = []
        if permission == 1:
            # We have to add in every Public source repository in only this case
            project_ids.extend([x[0] for x in SourceRepository.objects.filter(anonymous_access=True).values_list('id')])
        project_ids.extend([x[0] for x in RepositoryUser.objects.filter(user=user, permission__gte=permission).values_list('source_repository_id')])
        
        group_ids = [x[0] for x in user.groups.all().values_list('id')]
        repo_ids = [x[0] for x in RepositoryGroup.objects.filter(
                                permission__gte=permission, 
                                group__id__in=group_ids).values_list('source_repository_id')]
        project_ids.extend(repo_ids)
        return super(SourceRepositoryManager, self).get_query_set().filter(pk__in=project_ids).order_by('name')

class SourceRepository(models.Model):
    """
    A version controlled source code repository
    """
    name = models.SlugField(_("Name"))
    summary = models.CharField(_('Summary'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True,null=True)
    vc_system = models.IntegerField(_("Version Control System"), choices=VC_TYPE_CHOICES)
    anonymous_access = models.BooleanField(_("Allow Anonymous Viewing"), default=True)
    repo_template = models.CharField(_("Initial Repository Template"), 
        blank=True, choices=settings.get_repo_template_choices(), 
        max_length=255,
        help_text="Import this template into the repository when it is created. "\
                  "Changing it afterwards has no effect.")
    repo_path = models.CharField(editable=False, max_length=255)
    repo_url = models.CharField(editable=False, max_length=255)
    current_rev = models.CharField(blank=True, max_length=50, editable=False)
    previous_rev = models.CharField(blank=True, max_length=50, editable=False)
    
    class Meta:
        verbose_name = _("Source Repository")
        verbose_name_plural = _("Source Repositories")
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    objects = SourceRepositoryManager()
    
    def __init__(self, *args, **kwargs):
        """
        When a :class:`SourceRepository` object is instantiated and the object
        has selected a version control system, it sets up the ``self._vcs`` 
        attribute to the :class:`VCSClass` implementation, else set it to ``None``
        """
        super(SourceRepository, self).__init__(*args, **kwargs)
        # Select the appropriate VCS class from the VCS dictionary and instantiate it
        if self.vc_system:
            VCSClass = VCS[self.vc_system]
            self._vcs = VCSClass(self.name, self.anonymous_access, self.repo_template)
        else:
            self._vcs = None
    
    @models.permalink
    def get_absolute_url(self):
        """
        The path to the repository
        
        :rtype: ``string``
        """
        return self._vcs.get_absolute_url()
    
    
    def owners(self):
        """
        Get the users with owner access, including users that are in a
        :class:`RepositoryGroup` with owner access.
        
        :rtype: ``list`` of :class:`User`
        """
        users = self.repositoryuser_set.filter(permission=7).select_related()
        groups = self.repositorygroup_set.filter(permission=7).select_related()
        
        user_set = set([i.user for i in users])
        for group in groups:
            user_set.update(set(group.user_set.all()))
        return list(user_set)
    
    
    def members(self):
        """
        Get the users with write access, including users that are in a
        :class:`RepositoryGroup` with write access.
        
        :rtype: ``list`` of :class:`User`
        """
        users = self.repositoryuser_set.filter(permission=3).select_related()
        groups = self.repositorygroup_set.filter(permission=3).select_related()
        
        user_set = set([i.user for i in users])
        for group in groups:
            user_set.update(set(group.user_set.all()))
        return list(user_set)
    
    
    def user_is_owner(self, userobj):
        """
        Is this user an owner of the project?
        
        :param userobj: The :class:`User` to test
        :type userobj: :class:`User`
        :returns: ``True`` if the :class:`User` is an owner
        :rtype: ``boolean``
        """
        try:
            repousr = self.repositoryuser_set.get(user=userobj)
            return repousr.permission > 4
        except:
            pass
        
        for group in self.repositorygroup_set.filter(permission__gte=5):
            if userobj in group.group.user_set.all():
                return True
        
        return False
    
    
    def user_can_write(self, userobj):
        """
        Does this user have write access to this repository?
        
        :param userobj: The :class:`User` to test
        :type userobj: :class:`User`
        :returns: ``True`` if the :class:`User` can write to this repository
        :rtype: ``boolean``
        """
        try:
            repousr = self.repositoryuser_set.get(user=userobj)
            return repousr.permission > 2
        except:
            pass
        
        for group in self.repositorygroup_set.filter(permission__gte=3):
            if userobj in group.group.user_set.all():
                return True
        
        return False
    
    
    def user_can_read(self, userobj):
        """
        Does the user have read access to this repository?
        
        :param userobj: The :class:`User` to test
        :type userobj: :class:`User`
        :returns: ``True`` if the :class:`User` can read this repository
        :rtype: ``boolean``
        """
        if self.anonymous_access:
            return True
        try:
            repousr = self.repositoryuser_set.get(user=userobj)
            return True # If we have a user, it must have at least read
        except:
            pass
        
        for group in self.repositorygroup_set.all():
            if userobj in group.group.user_set.all():
                return True
        
        return False
    
    
    def move_to_public(self):
        """
        Move a repository from private to public. 
        
        Calls the instantiated version control object to do the low-level work,
        and then updates the :attr:`repo_path` and :attr:`repo_url`
        
        :returns: Nothing
        """
        self._vcs.make_public()
        self.repo_path = self._vcs.path
        self.repo_url = self._vcs.url
        
    
    def move_to_private(self):
        """
        Move a repository from public to private
        
        Calls the instantiated version control object to do the low-level work,
        and then updates the :attr:`repo_path` and :attr:`repo_url`
        
        :returns: Nothing
        """
        self._vcs.make_private()
        self.repo_path = self._vcs.path
        self.repo_url = self._vcs.url
        
    def save(self, force_insert=False, force_update=False):
        """
        We have to do a little maintenance before we save the record. It:
        
        * creates the repository if it is new
        * moves the repository from public to/from private as necessary
        * updates the :attr:`repo_path` and :attr:`repo_url`\ .
        """
        new = self.id is None
        if new:
            VCSClass = VCS[self.vc_system]
            self._vcs = VCSClass(self.name, self.anonymous_access, self.repo_template)
            self._vcs.create()
        if self._vcs.public != self.anonymous_access and not new:
            if self.anonymous_access:
                self._vcs.make_public()
            else:
                self._vcs.make_private()
        self.repo_path = self._vcs.path
        self.repo_url = self._vcs.url
        super(SourceRepository, self).save(force_insert, force_update)
    
    
    def delete(self):
        """
        Deletes the source repository before it deletes the record.
        """
        # Delete the source repository here
        self._vcs.delete()
        super(SourceRepository, self).delete()
    
    
    def list(self, path="/"):
        """
        Return a directory listing from the given repository path. **Not Implemented Yet**
        """
        pass


class RemoteSourceRepository(models.Model):
    """
    A source code repository on a remote server to which updates should be pushed.
    
    Pushing to a mirror on GitHub or LaunchPad is a common use.
    """
    repo = models.ForeignKey('SourceRepository', verbose_name=_('Repository'))
    name = models.SlugField(_('Name'))
    branch = models.CharField(_('Branch'), max_length=255, default='master')
    url = models.CharField(_('URL'), max_length=255)
    notes = models.TextField(_('Notes'), blank=True, 
        help_text=_('Notes about this remote repository'))
    active = models.BooleanField(_('Active'), default=True)
    
    def __unicode__(self):
        return '%s for %s' % (self.name, self.repo.name)
    
    def save(self, *args, **kwargs):
        VCSClass = VCS[self.repo.vc_system]
        self._vcs = VCSClass(self.repo.name, self.repo.anonymous_access, self.repo.repo_template)
        new = False
        if not self.id:
            new = True
        super(RemoteSourceRepository, self).save(*args, **kwargs)
        # Current only git is supported for remote repos
        if new and self.repo.vc_system == 3:
            self._vcs.add_remote(self.name, self.url, self.branch)
            generate_hooks(self.repo)
            
    def delete(self):
        VCSClass = VCS[self.repo.vc_system]
        self._vcs = VCSClass(self.repo.name, self.repo.anonymous_access, self.repo.repo_template)
        if self.repo.vc_system == 3:
            self._vcs.remove_remote(self.name)
            generate_hooks(self.name)
        super(RemoteSourceRepository, self).delete()
        
    class Meta:
        unique_together = ('repo', 'name')
        verbose_name_plural = 'Remote Source Repositories'

    
def generate_hooks(repo, htype='post-update', rtype='git'):
    if not isinstance(repo, SourceRepository):
        return
    if not htype:
        return
    # Only git repo's are supported atm.
    if rtype == 'git':
        try:
            import os, stat
            file_name = htype
            t = get_template('hooks/%s' % file_name)
            c = {'remote_repos': RemoteSourceRepository.objects.filter(repo__pk=repo.pk)}
            ret = render_to_string(t.name, c)
            file_path = '%s/hooks/%s' % (repo.repo_path, file_name)
            f = open(file_path, 'w+')
            f.write(ret)
            f.close()
            # set the premissions of the file
            os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        except:
            pass



class Metadata(models.Model):
    """
    Metadata for a SourceRepository. It is a key/value store. The value is a 
    freeform string. Examples of what one can use this metadata for:
    
    * Creating an install script.
    * Specifying dependencies
    * Current version
    
    The choices of metadata keys are configured in ``REPO_METADATA_KEYS``\ .
    A 'Version' key is added if it was not otherwise configured. A common choice
    for the metadata keys is the metadata for the Python Package Index.
    """
    source_repository = models.ForeignKey(SourceRepository)
    key = models.CharField(blank=False, null=False, max_length=255, choices=settings.METADATA_CHOICES)
    value = models.CharField(blank=True, null=True, max_length=255)
    
    def __unicode__(self):
        if self.value:
            return "%s = %s" % (self.key, self.value)
        else:
            return self.key


class RepositoryGroup(models.Model):
    """
    A group of people who have access to a repository and their access permissions.
    """
    
    source_repository = models.ForeignKey(SourceRepository)
    group = models.ForeignKey(Group)
    permission = models.IntegerField(_('Permission'), choices=PERM_CHOICES)
    
    def __unicode__(self):
        out = u"%s of %s with %s permission" % (self.group, 
                self.source_repository, self.get_permission_display())
        return out


class RepositoryUser(models.Model):
    """
    A User of a repository and that person's access permissions.
    """
    
    source_repository = models.ForeignKey(SourceRepository)
    user = models.ForeignKey(User)
    permission = models.IntegerField(_('Permission'), choices=PERM_CHOICES)
    
    def __unicode__(self):
        out = u"%s of %s with %s permission" % (self.user, 
                self.source_repository, self.get_permission_display())
        
        return out
