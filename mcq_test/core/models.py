from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=250, null=False)
    age = models.IntegerField(null=False)
    phone = models.CharField(unique=True, max_length=15, null=False)

class Exam(models.Model):
    topic = models.CharField(max_length=250, null=False)

class ExamQuestion(models.Model):
    question = models.TextField(null=False)
    exam_id = models.ForeignKey(Exam, on_delete=CASCADE, null=False)
    

class QuestionChoice(models.Model):
    content = models.TextField(null=False)
    correct_answer = models.BooleanField(default=False)
    question_id = models.ForeignKey(ExamQuestion, on_delete=CASCADE, null=False)




