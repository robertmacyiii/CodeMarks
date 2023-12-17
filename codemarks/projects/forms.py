from django import forms
from .models import Project, ProjectFile

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'root_path', 'description',)