from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    last = 0

    def new():
        res = Question.objects.filter(pk__gt=QuestionManager.last)
        QuestionManager.last = max([question.pk for question in res])
        return res


    def popular():
        return Question.objects.order_by('-rating')[:5]


class Question(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    author = models.CharField(max_length=20, blank=False)
    likes = models.ManyToManyField(User, related_name='question_like_user')

    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField(blank=False)
    added_at = models.DateTimeField()
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)


       
