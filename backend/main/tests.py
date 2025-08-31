from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import (Question,
                     Answer)

from .services import AnswerService

import uuid

import json

class AnswerServiceTest(APITestCase):
    def setUp(self):
        question = Question.objects.create(text='Test question?')
        self.question_id = question.id

    def test_create_answer(self):
        user_id = uuid.uuid4()
        text = 'Test answer'
        answer = AnswerService().create(question=Question.objects.get(pk=self.question_id),
                                        validated_data={'user_id': user_id,
                                                        'text': text})
        self.assertEqual(answer.user_id, user_id)
        self.assertEqual(answer.id, 1)
        self.assertEqual(answer.text, text)
        self.assertEqual(answer.question_id.id, 1)

class AnswerViewSetTest(APITestCase):
    def setUp(self):
        question = Question.objects.create(text='Test question?')
        self.question_id = question.id
        answer = AnswerService().create(question=Question.objects.get(pk=self.question_id),
                             validated_data={'user_id': uuid.uuid4(),
                                             'text': 'Test answer'})
        self.answer_id = answer.id
    
    def test_get_answer(self):
        client = APIClient()
        response = client.get(f'/answers/{self.answer_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        client = APIClient()
        response = client.delete(f'/answers/{self.answer_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Answer.objects.filter(pk=self.answer_id).exists())

class QuestionViewSetTest(APITestCase):
    def setUp(self):
        question = Question.objects.create(text='Test question?')
        self.question_id = question.id
        answer = AnswerService().create(question=Question.objects.get(pk=self.question_id),
                                        validated_data={'user_id': uuid.uuid4(),
                                                        'text': 'Test answer'})
        self.answer_id = answer.id

    def test_create_question(self):
        client = APIClient()
        questions_counter = Question.objects.all().count()
        response = client.post('/questions/',
                               json.dumps({'text': 'Another one?'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.all().count(), questions_counter + 1)

    def test_get_question(self):
        client = APIClient()
        response = client.get(f'/questions/{self.question_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_questions(self):
        client = APIClient()
        response = client.get(f'/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_question(self):
        client = APIClient()
        response = client.delete(f'/questions/{self.question_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(pk=self.question_id).exists())
        self.assertFalse(Answer.objects.filter(pk=self.answer_id).exists())

    def test_create_answer(self):
        client = APIClient()
        response = client.post(f'/questions/{self.question_id}/answers/',
                                json.dumps({'text': 'Test answer',
                                            'question_id': self.question_id,
                                            'user_id': str(uuid.uuid4())}),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_answers_with_same_user(self):
        client = APIClient()
        answers_counter = Answer.objects.all().count() 
        content = json.dumps({'text': 'Test answer',
                              'question_id': self.question_id,
                              'user_id': str(uuid.uuid4())})
        for i in range(2):
            response = client.post(f'/questions/{self.question_id}/answers/',
                                   content,
                                   content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Answer.objects.all().count(), answers_counter + 2)


    def test_create_answer_with_missing_question(self):
        client = APIClient()
        response = client.post(f'/questions/999/answers/',
                                json.dumps({'text': 'Test answer',
                                            'question_id': 999,
                                            'user_id': str(uuid.uuid4())}),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_question_with_missing_data(self):
        client = APIClient()
        response = client.post('/questions/',
                               json.dumps({}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_question_with_wrong_data(self):
        client = APIClient()
        response = client.post('/questions/',
                               json.dumps({'text': ''}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_answer_with_missing_data(self):
        client = APIClient()
        response = client.post(f'/questions/{self.question_id}/answers/',
                                json.dumps({'text': '',
                                            'user_id': str(uuid.uuid4())}),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(f'/questions/{self.question_id}/answers/',
                                json.dumps({'text': 'Test answer',
                                            'user_id': ''}),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)