from django.urls import path
from . import views
from .consumer import create_consumer
import threading

urlpatterns = [
    path('exam-result/<int:exam_id>', views.exam_result),
    path('exam-average-score/<int:exam_id>', views.average_score_per_topic),
    path('student-average-score/<int:student_id>', views.average_score_per_student),
    path('exam-highest-score/<int:exam_id>', views.highest_score_per_topic),
]

t = threading.Thread(target=create_consumer)
t.start()


