from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home-page'),
    path('codedevelopment', views.get_code_development, name='code_development'),
    path('executionhistory', views.get_execution_history, name='execution_history'),
    path('codeinventory',views.code_inventory,name='code_inventory'),
    path('ajax/load-projects/', views.load_projects, name='ajax_load_projects')
]