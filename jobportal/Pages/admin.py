from django.contrib import admin
from Pages.models import Assessment,Question

# Register your models here.
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
  list_display = ('title', 'duration',)
  
  
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ('question',)