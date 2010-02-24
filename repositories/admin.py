from django import forms
from django.contrib import admin
from models import SourceRepository, RepositoryUser, Metadata, \
                    RepositoryGroup, RemoteSourceRepository
from django.conf import settings

if 'objectpermissions' in settings.INSTALLED_APPS:
    from objectpermissions.admin import TabularUserPermInline, TabularGroupPermInline
    repo_admin_inlines = [TabularUserPermInline, TabularGroupPermInline, MetadataInline, RemoteRepositoryInline]
else:
    repo_admin_inlines=[UserInline, GroupInline, MetadataInline, RemoteRepositoryInline]

class UserInline(admin.TabularInline):
    model=RepositoryUser

class GroupInline(admin.TabularInline):
    model=RepositoryGroup

class MetadataInline(admin.TabularInline):
    model=Metadata

class RemoteRepositoryForm(forms.ModelForm):
    class Meta:
        exclude = ('notes',)
        model=RemoteSourceRepository

class RemoteRepositoryInline(admin.TabularInline):
    form=RemoteRepositoryForm
    model=RemoteSourceRepository

class SourceRepositoryAdmin(admin.ModelAdmin):
    list_filter = ('anonymous_access', 'vc_system', 'inactive',)
    list_display = ('name', 'vc_system', 'anonymous_access', 'inactive',)
    list_editable = ('anonymous_access', 'inactive')
    ordering = ('name', 'vc_system', 'anonymous_access', )
    search_fields = ('name', 'description', 'summary')
    inlines = repo_admin_inlines

admin.site.register(SourceRepository, SourceRepositoryAdmin)
