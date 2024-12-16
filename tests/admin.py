from django.contrib import admin

from .models import Test, Question,Option,AssignedTest,TestResult,Answer

class TestAdmin(admin.ModelAdmin):
    pass
    #list_display = ('email','role')

class QuestionAdmin(admin.ModelAdmin):
    pass
    #list_display = ('user', 'career')
class OptionAdmin(admin.ModelAdmin):
    pass
    #list_display = ('email','role')

class AssignedTestAdmin(admin.ModelAdmin):
    list_display = ('student','test')
class TestResultAdmin(admin.ModelAdmin):
    pass
    #list_display = ('email','role')

class AnswerAdmin(admin.ModelAdmin):
    pass
    #list_display = ('user', 'career')


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(AssignedTest, AssignedTestAdmin)
admin.site.register(TestResult, TestResultAdmin)
admin.site.register(Answer, AnswerAdmin)
