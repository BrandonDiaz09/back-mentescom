# Generated by Django 5.1.3 on 2024-12-12 09:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities_resources', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_activities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activityprogress',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='activities_resources.activity'),
        ),
        migrations.AddField(
            model_name='activityprogress',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignedactivity',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_activities', to='activities_resources.activity'),
        ),
        migrations.AddField(
            model_name='assignedactivity',
            name='assigned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_activities_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignedactivity',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_activities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resource',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_resources', to=settings.AUTH_USER_MODEL),
        ),
    ]
