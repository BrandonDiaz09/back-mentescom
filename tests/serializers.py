from rest_framework import serializers
from .models import Test, Question, Option, AssignedTest, TestResult, Answer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'value', 'order']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # Incluye todas las opciones de la pregunta.

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'order', 'options']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'questions']
        
class TestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name']

class AssignedTestSerializer(serializers.ModelSerializer):
    test = TestSerializer()

    class Meta:
        model = AssignedTest
        fields = ['id', 'test', 'student', 'assigned_by', 'assigned_at']

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'test', 'student', 'total_score', 'submitted_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'selected_option', 'value']
