from typing import OrderedDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Exam, QuestionChoice, Student, ExamQuestion
from .serializers import QuestionChoiceSerializer, StudentSerializer, ExamSerializer, ExamQuestionSerializer
from .producer import publish_message
import random



@api_view(['GET'])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_exams(request):
    exams = Exam.objects.all()
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_exam(request):
    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_question(request):
    serializer = ExamQuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_choice(request):
    serializer = QuestionChoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def exam_enroll(request, exam_id):
    # get exam if exists
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    phone = request.data.get('phone',False)
    if phone:
        student = Student.objects.filter(phone=phone)[:1]
        if not student.exists():
            student_ser = StudentSerializer(data=request.data)
            if student_ser.is_valid():
                student_ser.save()
                student = student_ser.data
            else:
                return Response(student_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            student_ser = StudentSerializer(student, many=True)
            student = student_ser.data[0]


        questions = ExamQuestion.objects.filter(exam_id=exam_id)
        question_ser = ExamQuestionSerializer(questions, many=True)
        questions = question_ser.data
        random.shuffle(questions)
        for q in questions:
            choices = QuestionChoice.objects.filter(question_id=q.get('id'))
            choices_ser = QuestionChoiceSerializer(choices,many=True)
            choices = choices_ser.data
            random.shuffle(choices)
            q['choices'] = choices

        res = OrderedDict()
        res['student_id'] = student.get('id')
        res['exam_id'] =exam_id
        res['questions'] = questions
        return Response(res)

    else:
        return Response({"error":"phone is required"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def exam_submit(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({ "error": "exam not found"},status=status.HTTP_404_NOT_FOUND)

    try:
        student_id = request.data['student_id']
        answers = request.data['answers']
    except KeyError:
        return Response({ "error": "student_id and answers is required"}, status=status.HTTP_400_BAD_REQUEST)


    if type(student_id) != int:
        return Response({ "error": "student_id must be int"}, status=status.HTTP_400_BAD_REQUEST)

    if type(answers) != list or not all(type(ans)==int for ans in answers):
        return Response({ "error": "answers must be list of int"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({ "error": "student not found"},status=status.HTTP_404_NOT_FOUND)
    
    questions_no = ExamQuestion.objects.filter(exam_id=exam_id).count()
    data_to_publish = {'student_id': student_id , 'exam_id': exam_id, 'answers': [], 'question_no': questions_no }
    for ans in answers:
        choice = QuestionChoice.objects.get(id=ans)
        choice = QuestionChoiceSerializer(choice,many=False).data
        data_to_publish['answers'].append(choice)
    publish_message(data_to_publish)
    return Response({"message": "Exam submitted succesfully"})
        
    
    


