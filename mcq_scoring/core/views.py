from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ExamScore
from .serializers import ExamScoreSerializer
from django.db.models import Avg, Max

@api_view(['GET'])
def exam_result(request,exam_id):
    score = ExamScore.objects.filter(exam_id=exam_id).order_by('-id')
    if score.exists():
        serializer = ExamScoreSerializer(score, many=True)
        return Response(serializer.data[0])
    else:
        return Response({'error': 'Student did not take this exam yet'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def average_score_per_topic(request,exam_id):
    score = ExamScore.objects.filter(exam_id=exam_id).aggregate(Avg('score'))
    return Response(score)

@api_view(['GET'])
def average_score_per_student(request,student_id):
    score = ExamScore.objects.filter(student_id=student_id).aggregate(Avg('score'))
    return Response(score)

@api_view(['GET'])
def highest_score_per_topic(request,exam_id):
    score = ExamScore.objects.filter(exam_id=exam_id).aggregate(Max('score'))
    return Response(score)