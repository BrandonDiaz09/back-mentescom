from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Activity, AssignedActivity, ActivityProgress, Resource
from .serializers import ActivitySerializer, AssignedActivitySerializer, ActivityProgressSerializer, ResourceSerializer, ActivityListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now

class ActivityListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivityListSerializer

class AssignedActivityListView(ListAPIView):
    serializer_class = AssignedActivitySerializer

    def get_queryset(self):
        return AssignedActivity.objects.filter(student=self.request.user)

class ActivityProgressCreateView(CreateAPIView):
    serializer_class = ActivityProgressSerializer


class AssignedResourceListView(ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resource.objects.filter(assigned_to=self.request.user)
    
class UpdateActivityProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, activity_id):
        try:
            # Verifica que la actividad esté asignada al usuario
            assigned_activity = AssignedActivity.objects.filter(
                activity_id=activity_id, student=request.user
            ).first()

            if not assigned_activity:
                return Response({"detail": "Actividad no asignada."}, status=404)

            # Busca el progreso de la actividad
            progress, created = ActivityProgress.objects.get_or_create(
                activity_id=activity_id, student=request.user
            )

            # Si ya está completada, permite desmarcarla
            if progress.completed_at:
                progress.completed_at = None
                progress.save()
                return Response({"detail": "Actividad marcada como no completada."})

            # Marca la actividad como completada
            progress.completed_at = now()
            progress.save()
            return Response({"detail": "Actividad marcada como completada."})
        except Exception as e:
            return Response({"detail": str(e)}, status=400)