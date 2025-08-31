from rest_framework import routers

from .views import (QuestionViewSet,
                    AnswerViewSet)

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)