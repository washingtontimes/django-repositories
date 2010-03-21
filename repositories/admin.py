from django import forms
from django.contrib import admin
from models import SourceRepository, Metadata, RemoteSourceRepository
from django.conf import settings


class MetadataInline(admin.TabularInline):
    model=Metadata

class RemoteRepositoryForm(forms.ModelForm):
    class Meta:
        exclude = ('notes',)
        model=RemoteSourceRepository

class RemoteRepositoryInline(admin.TabularInline):
    form=RemoteRepositoryForm
    model=RemoteSourceRepository


if 'objectpermissions' in settings.INSTALLED_APPS:
    USE_OBJECT_PERMS = True
    from objectpermissions.admin import TabularUserPermInline, TabularGroupPermInline
    if 'projects' in settings.INSTALLED_APPS:
        repo_admin_inlines = [MetadataInline, RemoteRepositoryInline]
    else:
        repo_admin_inlines = [TabularUserPermInline, TabularGroupPermInline, MetadataInline, RemoteRepositoryInline]
else:
    USE_OBJECT_PERMS = False
    from models import RepositoryUser, RepositoryGroup
    
    class UserInline(admin.TabularInline):
        model=RepositoryUser
    
    class GroupInline(admin.TabularInline):
        model=RepositoryGroup
    
    repo_admin_inlines=[UserInline, GroupInline, MetadataInline, RemoteRepositoryInline]


class SourceRepositoryAdmin(admin.ModelAdmin):
    list_filter = ('anonymous_access', 'vc_system', 'inactive',)
    list_display = ('name', 'vc_system', 'anonymous_access', 'inactive',)
    list_editable = ('anonymous_access', 'inactive')
    ordering = ('name', 'vc_system', 'anonymous_access', )
    search_fields = ('name', 'description', 'summary')
    inlines = repo_admin_inlines
    popup_fields = ('name', 'vc_system', 'repo_template')
    
    def save_model(self, request, obj, form, change):
        super(SourceRepositoryAdmin, self).save_model(request, obj, form, change)
        if not change and USE_OBJECT_PERMS:
            request.user.grant_object_perm(obj, ['read','write','owner'])
    
    def queryset(self, request):
        """
        Filter the objects displayed in the change_list to show only those with
        write or owner permissions
        """
        if request.user.is_superuser:
            return super(SourceRepositoryAdmin, self).queryset(request)
        return SourceRepository.objects.get_for_user(request.user, 6) # write = 2, owner = 4
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Return a different set of fields if the form is shown in a popup window
        versus a normal window. To provide better integration with a project
        manager, which will presumably be managing certain information, we 
        include only the bare necessity of fields in the popup menu.
        
        This is pretty much copied from Django source, with a bit to make it work
        with 1.1 as well as 1.2.
        
        Returns a Form class for use in the admin add view. This is used by
        add_view and change_view.
        """
        from django.contrib.admin.util import flatten_fieldsets
        from django.forms.models import modelform_factory
        from django.utils.functional import curry
        
        if request.REQUEST.has_key('_popup'):
            fields = flatten_fieldsets([(None, {'fields': self.popup_fields})])
        elif self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(kwargs.get("exclude", []))
        
        if hasattr(self, 'get_readonly_fields'):
            exclude.extend(self.get_readonly_fields(request, obj))
        # if exclude is an empty list we pass None to be consistant with the
        # default on modelform_factory
        exclude = exclude or None
        defaults = {
            "form": self.form,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": curry(self.formfield_for_dbfield, request=request),
        }
        defaults.update(kwargs)
        return modelform_factory(self.model, **defaults)


admin.site.register(SourceRepository, SourceRepositoryAdmin)
