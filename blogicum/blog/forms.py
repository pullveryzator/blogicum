from django import forms

from django.core.exceptions import ValidationError

from django.core.mail import send_mail

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {'post': forms.DateInput(attrs={'type': 'date'})}

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
