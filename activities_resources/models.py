from django.db import models
from users.models import User

class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Resource(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    assigned_to = models.ManyToManyField(User, related_name='assigned_resources')

    def __str__(self):
        return self.title

class AssignedActivity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='assigned_activities')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_activities')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_activities_by')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity.title} assigned to {self.student.email}"

class ActivityProgress(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='progress')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_progress')
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Progress for {self.activity.title} by {self.student.email}"

