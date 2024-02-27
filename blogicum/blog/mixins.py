from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from blog.models import Comment, Post
from .forms import CommentForm, PostForm


class SuccessUrlToProfileMixin:
    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username}
                       )


class SuccessUrlToPostMixin:
    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']}
                       )


class PostRequiredAttrsMixin:
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostFormValidMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostFormMixin:
    form_class = PostForm


class CommentFormMixin:
    form_class = CommentForm


class CommentRequiredAttrsMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'


class PostUpdateDeleteMixin(LoginRequiredMixin, PostRequiredAttrsMixin):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateDeleteMixin(LoginRequiredMixin,
                               CommentRequiredAttrsMixin,
                               SuccessUrlToPostMixin):
    def get_object(self):
        return get_object_or_404(
            Comment,
            author=self.request.user,
            post_id=self.kwargs['post_id'],
            id=self.kwargs['comment_id'])
