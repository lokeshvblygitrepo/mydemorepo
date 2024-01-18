from . data_api import BitBucket_API as BB
from . data_sql import SQL
from . forms import ProjectForm
from function_library.qacomplete.project import QACProjectAPI


def home(request):
    return render(request, "reporting_app/home.html")

def get_code_development(request):
    return render(request, "reporting_app/code_development.html")

def get_execution_history(request):
    return render(request, "reporting_app/execution_history.html")

from django.http import HttpResponseRedirect
from django.shortcuts import render


from django.views.generic import CreateView
from .models import Category,Project

class ProjectView(CreateView):
    model = Project
    form_class = ProjectForm


from .models import Project
def load_projects(request):
    category_id = request.GET.get('category')
    projects = Project.objects.filter(category_id=category_id).order_by('project')

    return render(request, 'reporting_app/project_dropdown_list_options.html',{'projects':projects})

def code_inventory(request):
    form = ProjectForm

    category_id = request.GET.get('category')
    project_id = request.GET.get('project')

    if project_id is not None:

        category_name = Category.objects.get(id=category_id).category
        project = Project.objects.get(id=project_id)
        project_name = project.project
        repo = project.repo
        branch = project.branch
        qac_project_name = project.qac
        path = project.path
        run_type = project.run_type

        data = BB(repo, branch, path)

        project_id = QACProjectAPI().get_project_id(qac_project_name)

        tests_id = data.get_test(run_type)
        tests = SQL(project_id, tests_id).get_test_title()

        if tests is not None:

            context = {
                'form':form,
                'testlist':tests,
                'category':category_name,
                'project':project_name,
                'repo':repo,
                'branch':branch
            }


            return render(request, 'reporting_app/code_inventory.html', context)
    else:
        return render(request,'reporting_app/code_inventory.html', {'form':form})





