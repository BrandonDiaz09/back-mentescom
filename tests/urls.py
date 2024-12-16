from django.urls import path
from .views import TestListView, AssignedTestListView, TestResultCreateView, AssignedTestDetailView, AssignTestView

urlpatterns = [
    path('tests/', TestListView.as_view(), name='test-list'),
    path('assigned-tests/', AssignedTestListView.as_view(), name='assigned-test-list'),
    path('submit-result/', TestResultCreateView.as_view(), name='test-result-create'),
    path('assigned-test/<int:test_id>/', AssignedTestDetailView.as_view(), name='assigned-test-detail'),
    path('assign-test/', AssignTestView.as_view(), name='assign-test'), 
]
