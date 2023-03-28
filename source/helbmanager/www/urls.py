from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('project/<int:pk>/', project_detail, name='project-detail'),
    path('project/<int:pk>/update/', project_update, name='project-update'),
    path('project/<int:pk>/new key/', generate_new_key, name='generate-new-key'),
    path('project/<int:pk>/timeline', timeline, name='project-timeline')
]
