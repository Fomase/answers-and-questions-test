from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   ListModelMixin,
                                   DestroyModelMixin)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .models import (Question,
                     Answer) 

from .serializers import (QuestionSerializer,
                          QuestionDetailSerializer,
                          AnswerSerializer)

from .services import AnswerService

class QuestionViewSet(CreateModelMixin,
                      RetrieveModelMixin,
                      ListModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionSerializer
        return QuestionDetailSerializer
    
    @action(detail=True, methods=['post'], url_path='answers')
    def create_answer(self, request, pk=None) -> Response:
        question = get_object_or_404(Question, pk=pk)
        input_serializer = AnswerSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        answer = AnswerService().create(question=question, validated_data = input_serializer.validated_data)
        output_serializer = AnswerSerializer(answer)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED)
        

class AnswerViewSet(RetrieveModelMixin,
                    DestroyModelMixin,
                    GenericViewSet):  
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer