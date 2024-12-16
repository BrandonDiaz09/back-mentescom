from django.db import models
from users.models import User

class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    SINGLE_CHOICE = 'SINGLE_CHOICE'
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE'
    RATING = 'RATING'
    QUESTION_TYPE_CHOICES = [
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (RATING, 'Rating'),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Question {self.order} in {self.test.name}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    value = models.FloatField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Option {self.order} for {self.question.text}"

class AssignedTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='assigned_tests')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tests')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tests_by')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.name} assigned to {self.student.email}"

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    total_score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.test.name} by {self.student.email}"

class Answer(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='answers')
    value = models.FloatField()

    def __str__(self):
        return f"Answer for {self.question.text}"