from django import forms

from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {'pub_date': forms.DateInput(attrs={'type': 'date'})}

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)
