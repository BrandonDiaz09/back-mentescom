from django.urls import path
from .views import ActivityListView, AssignedActivityListView, ActivityProgressCreateView,AssignedResourceListView, UpdateActivityProgressView

urlpatterns = [
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('assigned-activities/', AssignedActivityListView.as_view(), name='assigned-activity-list'),
    path('progress/', ActivityProgressCreateView.as_view(), name='activity-progress-create'),
    path('resources/assigned/', AssignedResourceListView.as_view(), name='assigned-resources'),
    path('progress/<int:activity_id>/', UpdateActivityProgressView.as_view(), name='update-activity-progress'),
]
