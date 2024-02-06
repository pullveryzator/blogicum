from django.views.generic import (
    CreateView, DeleteView,
    DetailView, ListView,
    UpdateView
    )

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from blog.models import Post, Category, Profile
from .forms import PostForm

POSTS_PER_PAGE = 10
User = get_user_model()


def get_posts_qs():
    current_datetime = timezone.now()
    return Post.objects.select_related(
        'category').filter(
            is_published=True,
            pub_date__lte=current_datetime,
            category__is_published=True
    )


def post_detail(request, id):
    template = 'blog/detail.html'
    post_detail = get_object_or_404(get_posts_qs(), pk=id)
    context = {'post': post_detail}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_list_or_404(
        get_posts_qs().filter(
            category__slug=category_slug).order_by('-pub_date')
    )
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = User.objects.filter(username=username)
    context = {'profile': profile}
    return render(request, template, context)


class PostListView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = '-pub_date'
    paginate_by = POSTS_PER_PAGE


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'blog/create.html'
    model = Post
    success_url = reverse_lazy('blog:list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


