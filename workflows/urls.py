from django.urls import path
from . import views

urlpatterns = [
    path('parse/', views.ParseWorkflowView.as_view(), name='parse-workflow'),
    path('', views.WorkflowListCreateView.as_view(), name='workflow-list-create'),
    path('<int:workflow_id>/', views.WorkflowDetailView.as_view(), name='workflow-detail'),
    path('<int:workflow_id>/run/', views.WorkflowRunView.as_view(), name='workflow-run'),
]
