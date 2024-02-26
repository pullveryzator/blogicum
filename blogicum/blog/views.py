from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Category, Comment, Post
from .forms import CommentForm, PostForm, ProfileForm

POSTS_PER_PAGE = 10
User = get_user_model()


def paginate(queryset, request):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


class SuccessUrlToProfileMixin():
    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user}
                       )


class SuccessUrlToPostMixin():
    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']}
                       )


class PostRequireAttrsMixin():
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class CommentRequireAttrsMixin():
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'


class PostUpdateDeleteMixin(LoginRequiredMixin, PostRequireAttrsMixin):

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateDeleteMixin(LoginRequiredMixin,
                               CommentRequireAttrsMixin,
                               SuccessUrlToPostMixin):

    def get_object(self):
        return get_object_or_404(
            Comment,
            author=self.request.user,
            post_id=self.kwargs['post_id'],
            id=self.kwargs['comment_id'])


def get_posts_qs_by_category():
    current_datetime = timezone.now()
    return Post.objects.select_related(
        'category').filter(
            is_published=True,
            pub_date__lte=current_datetime,
            category__is_published=True).order_by(
                '-pub_date').annotate(
                comment_count=Count('comments')
    )


def get_posts_gs_by_author(username):
    return Post.objects.select_related(
        'author').filter(
            author__username=username).order_by(
                '-pub_date').annotate(
                    comment_count=Count('comments')
    )


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_posts_qs_by_category().filter(category__slug=category_slug)
    context = {'category': category, 'page_obj': paginate(posts, request)}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    if request.user.is_authenticated and request.user.username == username:
        posts = get_posts_gs_by_author(username)
    else:
        posts = get_posts_gs_by_author(username).filter(
            is_published=True,
            category__is_published=True
        )
    context = {'profile': profile, 'page_obj': paginate(posts, request)}
    return render(request, template, context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user}
                       )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    paginate_by = POSTS_PER_PAGE
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author == request.user:
            pass
        elif instance.is_published is False:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related(
                'author').order_by(
                    'created_at')
        )
        return context


class PostListView(ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE
    queryset = get_posts_qs_by_category()


class PostCreateView(LoginRequiredMixin,
                     SuccessUrlToProfileMixin,
                     PostRequireAttrsMixin,
                     CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostUpdateDeleteMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(PostUpdateDeleteMixin,
                     SuccessUrlToProfileMixin,
                     DeleteView):
    pass


class CommentCreateView(LoginRequiredMixin,
                        SuccessUrlToPostMixin,
                        CommentRequireAttrsMixin,
                        CreateView):
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.current_post
        return super().form_valid(form)


class CommentUpdateView(CommentUpdateDeleteMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentUpdateDeleteMixin, DeleteView):
    pass
