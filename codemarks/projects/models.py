from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    root_path = models.CharField(max_length=255, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    last_read_commit = models.CharField(max_length=255)
    current_commit = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name

