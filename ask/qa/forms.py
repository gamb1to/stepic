from hashlib import md5

from django.forms import ModelForm
from django.forms import CharField


from qa.models import Question
from qa.models import Answer
from qa.models import User


class AskForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'author']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
    
    def save(self, question):
        self.cleaned_data['question'] = question
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password).hexdigest()
