from rest_framework import serializers
from .models import Student
from .models import Exam
from .models import ExamQuestion
from .models import QuestionChoice

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestion
        fields = '__all__'

class QuestionChoiceSerializer(serializers.ModelSerializer):
    def validate(self, attrs): 
        if attrs.get('correct_answer', False) and QuestionChoice.objects.filter(question_id=attrs['question_id'], correct_answer=True).exists():
            raise serializers.ValidationError('A correct answer already exists for this question.')
        return super().validate(attrs)

    class Meta:
        model = QuestionChoice
        fields = '__all__'

