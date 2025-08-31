from .models import (Question,
                     Answer)

class AnswerService():
    def __init__(self, instance = None):
        self.instance = instance

    def create(self, validated_data: dict, question: Question) -> Answer:
        self.instance = Answer.objects.create(question_id = question, **validated_data)
        return self.instance