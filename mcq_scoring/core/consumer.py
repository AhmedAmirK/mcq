from kafka import KafkaConsumer
from django.conf import settings
from .serializers import ExamScoreSerializer
import json

TOPIC = 'exam_submit'

def create_consumer():
    consumer = KafkaConsumer(TOPIC, bootstrap_servers=settings.KAFKA_SERVER,
                            value_deserializer=lambda d: json.loads(d.decode('utf-8')))

    for message in consumer:
        #calculate score
        message = message.value
        answers = message.get('answers')
        score = 0
        for ans in answers:
            if ans.get('correct_answer'):
                score += 1
        question_no = message.get('question_no')
        score = (score/question_no) * 100
        student_id = message.get('student_id')
        exam_id = message.get('exam_id')
        serializer = ExamScoreSerializer(data={'exam_id': exam_id, 'student_id': student_id, 'score': score})
        if serializer.is_valid():
            serializer.save()

    