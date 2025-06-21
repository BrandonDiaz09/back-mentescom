from django.shortcuts import render
from django.db.models import Q, Exists, OuterRef
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Test, AssignedTest, TestResult, Answer
from .serializers import TestSerializer, AssignedTestSerializer, TestResultSerializer, TestListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestListView(ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestListSerializer

class AssignedTestListView(ListAPIView):
    serializer_class = AssignedTestSerializer

    def get_queryset(self):
        user = self.request.user

        # Filtrar AssignedTest que no tengan un TestResult asociado
        queryset = AssignedTest.objects.annotate(
            has_result=Exists(
                TestResult.objects.filter(test=OuterRef('test'), student=user)
            )
        ).filter(Q(student=user) & Q(has_result=False))

        return queryset

class TestResultCreateView(CreateAPIView):
    serializer_class = TestResultSerializer

class AssignedTestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, test_id):
        # Busca el test asignado por su ID y el estudiante autenticado
        assigned_test = AssignedTest.objects.filter(test_id=test_id, student=request.user).first()
        if not assigned_test:
            return Response({"detail": f"Test no encontrado o no asignado a este usuario. {request.user}"}, status=404)

        # Serializa el test asignado con preguntas y opciones
        serializer = AssignedTestSerializer(assigned_test)
        return Response(serializer.data)
    
class TestResultCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        test_id = data.get("test_id")
        responses = data.get("responses", [])  # Lista de respuestas

        if not test_id or not responses:
            return Response({"detail": "Test ID y respuestas son requeridos."}, status=400)

        try:
            # Crea el resultado del test
            test = Test.objects.get(id=test_id)
            total_score = sum([response.get("value", 0) for response in responses])

            test_result = TestResult.objects.create(
                test=test, 
                student=request.user, 
                total_score=total_score
            )

            # Guarda cada respuesta individual
            for response in responses:
                Answer.objects.create(
                    test_result=test_result,
                    question_id=response["question_id"],
                    selected_option_id=response["selected_option_id"],
                    value=response["value"]
                )

            return Response({"detail": "Test enviado exitosamente.", "total_score": total_score}, status=201)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Test, AssignedTest
from users.models import User  # Importa el modelo de usuario
from rest_framework import status
from .serializers import AssignedTestSerializer

class AssignTestView(APIView):
    """
    Vista para asignar un test a un estudiante.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student_id = request.data.get("student_id")
        test_id = request.data.get("test_id")

        # Validación de datos
        if not student_id or not test_id:
            return Response({"detail": "student_id y test_id son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verificar si el usuario y el test existen
            student = User.objects.get(id=student_id)
            test = Test.objects.get(id=test_id)

            # Verificar si el test ya fue asignado al estudiante
            if AssignedTest.objects.filter(student=student, test=test).exists():
                return Response({"detail": "El test ya está asignado a este estudiante."}, status=status.HTTP_400_BAD_REQUEST)

            # Crear la asignación del test
            assigned_test = AssignedTest.objects.create(
                test=test,
                student=student,
                assigned_by=request.user  # La psicóloga autenticada asigna el test
            )

            serializer = AssignedTestSerializer(assigned_test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"detail": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Test.DoesNotExist:
            return Response({"detail": "Test no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TestResult, Answer
from .serializers import AnswerSerializer
from rest_framework import status

class TestResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, test_id):  # Ahora recibimos student_id y test_id de la URL
        try:
            # Buscar los resultados del test y validar si existen
            print(TestResult.objects.all())
            test_results = TestResult.objects.get(test_id=test_id, student_id=student_id)
            answers = Answer.objects.filter(test_result=test_results).select_related('question', 'selected_option')

            # Formatear la respuesta
            data = {
                "total_score": test_results.total_score,
                "submitted_at": test_results.submitted_at,
                "answers": [
                    {
                        "question": answer.question.text,
                        "selected_option": answer.selected_option.text,
                        "value": answer.value
                    }
                    for answer in answers
                ]
            }
            return Response(data, status=200)

        except TestResult.DoesNotExist:
            return Response({"detail": "Resultados no encontrados."}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)  