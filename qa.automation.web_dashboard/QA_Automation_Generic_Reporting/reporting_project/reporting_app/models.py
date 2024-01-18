from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    project = models.CharField(max_length=50)
    repo = models.CharField(max_length=50, default='')
    branch = models.CharField(max_length=50,default='')
    qac = models.CharField(max_length=50,default='')
    path = models.CharField(max_length=50,default='')
    run_type = models.CharField(max_length=50,default='')

    def __str__(self):
        return self.project


