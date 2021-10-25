from django.db import models
from django.db.models.expressions import F
from django.db import models
# Create your models here.

class ExamScore(models.Model):
    exam_id = models.IntegerField(null=False)
    student_id = models.IntegerField(null=False)
    score = models.IntegerField(null=False)

class StudentAverage(models.Model):
    student_id = models.IntegerField(null=False)
    average = models.FloatField(null=False)
    no_of_exams = models.IntegerField(default=0)
