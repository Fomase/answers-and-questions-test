from django.db import models

class Question(models.Model):
    text = models.TextField(blank=False,
                            null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question'

class Answer(models.Model):
    question_id = models.ForeignKey(to='Question',
                                    on_delete=models.CASCADE,
                                    null=False,
                                    related_name='answers')
    
    user_id = models.UUIDField(blank=False,
                               null=False) #Использовано решение без прямых связей в виду отсутствия таковых в базе данных 
    
    text = models.TextField(blank=False,
                            null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'answer'


