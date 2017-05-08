from django.db import models
from hashlib import md5


class User(models.Model):
    username = models.CharField(max_length=16, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=False, blank=False)

    def check_password(self, password):
        return md5(password).hexdigest() == self.password


class Session(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User)
    expires = models.DateTimeField()


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    likes = models.ManyToManyField(User, related_name='question_like_user')

    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField(blank=False)
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
