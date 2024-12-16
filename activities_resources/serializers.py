from rest_framework import serializers
from .models import Activity, Resource, AssignedActivity, ActivityProgress

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'file']

class ActivitySerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'resources']

class AssignedActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    completed_at = serializers.SerializerMethodField()

    class Meta:
        model = AssignedActivity
        fields = ['id', 'activity', 'student', 'assigned_by', 'assigned_at', 'completed_at']

    def get_completed_at(self, obj):
        # Obtener el progreso de la actividad para el estudiante
        progress = ActivityProgress.objects.filter(activity=obj.activity, student=obj.student).first()
        return progress.completed_at if progress else None


class ActivityProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityProgress
        fields = ['id', 'activity', 'student', 'completed_at']

class ActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title']
