from django.urls import path
from . import views

urlpatterns = [
    path('exam-create', views.create_exam),
    path('question-create', views.create_question),
    path('choice-create', views.create_choice),
    path('students-all', views.list_students),
    path('exams-all', views.list_exams),
    path('exam-enroll/<int:exam_id>', views.exam_enroll),
    path('exam-submit/<int:exam_id>', views.exam_submit),
    
]