from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/create/', task_create, name='task-create'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),

]
