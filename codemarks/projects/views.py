from django.shortcuts import render, redirect
from .models import Project, ProjectFile
from .forms import ProjectForm

def project_list(request):
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'project_list.html', {'projects': projects, 'form': form})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    files = ProjectFile.objects.filter(project=project)
    return render(request, 'project_detail.html', {'project': project, 'files': files})
