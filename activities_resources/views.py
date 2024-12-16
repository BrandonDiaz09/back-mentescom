from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Activity, AssignedActivity, ActivityProgress, Resource, User
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
        
class AssignActivityView(APIView):
    """
    Vista para asignar una actividad a un estudiante.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student_id = request.data.get("student_id")
        activity_id = request.data.get("activity_id")

        # Validar que los datos sean proporcionados
        if not student_id or not activity_id:
            return Response(
                {"detail": "student_id y activity_id son requeridos."},
                status=400,
            )

        try:
            # Verificar si el usuario (estudiante) y la actividad existen
            student = User.objects.get(id=student_id)
            activity = Activity.objects.get(id=activity_id)

            # Verificar si la actividad ya fue asignada al estudiante
            if AssignedActivity.objects.filter(student=student, activity=activity).exists():
                return Response(
                    {"detail": "La actividad ya está asignada a este estudiante."},
                    status=400,
                )

            # Asignar la actividad al estudiante
            assigned_activity = AssignedActivity.objects.create(
                student=student, activity=activity, assigned_by=request.user
            )

            serializer = AssignedActivitySerializer(assigned_activity)
            return Response(serializer.data, status=201)

        except User.DoesNotExist:
            return Response({"detail": "Estudiante no encontrado."}, status=404)
        except Activity.DoesNotExist:
            return Response({"detail": "Actividad no encontrada."}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
