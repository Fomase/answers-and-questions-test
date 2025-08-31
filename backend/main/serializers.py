from rest_framework import serializers

from .models import (Question,
                     Answer)

class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id',
                  'question_id',
                  'user_id',
                  'text',
                  'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id',
                  'text',
                  'created_at']
        
class QuestionDetailSerializer(QuestionSerializer):
    answers = AnswerSerializer(many=True,
                               read_only=True)

    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ['answers']