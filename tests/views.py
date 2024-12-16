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
