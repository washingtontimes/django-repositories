from django import forms
from django.contrib import admin
from models import SourceRepository, RepositoryUser, Metadata, \
                    RepositoryGroup, RemoteSourceRepository


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
    list_filter = ('anonymous_access', 'vc_system')
    list_display = ('name', 'vc_system', 'anonymous_access', )
    ordering = ('name', 'vc_system', 'anonymous_access', )
    search_fields = ('name', 'description', 'summary')
    inlines=[UserInline, GroupInline, MetadataInline, RemoteRepositoryInline]

admin.site.register(SourceRepository, SourceRepositoryAdmin)
