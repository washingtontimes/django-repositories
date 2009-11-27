from django import forms
from models import SourceRepository

class SourceRepositoryForm(forms.ModelForm):
    class Meta:
        model = SourceRepository
