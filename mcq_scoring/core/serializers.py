from rest_framework import serializers
from .models import ExamScore

class ExamScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamScore
        fields = '__all__'