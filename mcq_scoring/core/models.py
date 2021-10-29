from django.db import models
from django.db.models.expressions import F
from django.db import models
# Create your models here.

class ExamScore(models.Model):
    exam_id = models.IntegerField(null=False)
    student_id = models.IntegerField(null=False)
    score = models.FloatField(null=False)
