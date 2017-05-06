from django.forms import ModelForm
from django.forms import CharField

from qa.models import Question
from qa.models import Answer


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
