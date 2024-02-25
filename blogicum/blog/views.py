from django.views.generic import (
    CreateView, DeleteView,
    DetailView, ListView,
    UpdateView
    )

from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
    )
from django.utils import timezone
from django.core.paginator import Paginator

from blog.models import Post, Category, Comment
from .forms import PostForm, CommentForm, ProfileForm

POSTS_PER_PAGE = 10
User = get_user_model()
current_datetime = timezone.now()


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.select_related(
        'category').filter(
            is_published=True,
            pub_date__lte=current_datetime,
            category__is_published=True,
            category__slug=category_slug).order_by(
                '-pub_date').annotate(
                    comment_count=Count('comments'))

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'category': category}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    if request.user.is_authenticated and request.user.username == username:
        posts = Post.objects.select_related(
                'author').filter(
                author__username=username).order_by(
                    '-pub_date').annotate(
                        comment_count=Count('comments'))
    else:
        posts = Post.objects.select_related(
            'author').filter(
                is_published=True,
                pub_date__lte=current_datetime,
                category__is_published=True,
                author__username=username).order_by(
                    '-pub_date').annotate(
                        comment_count=Count('comments'))
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, template, context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
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
        if instance.author != request.user:
            instance = get_object_or_404(Post, pk=kwargs['post_id'],
                                         is_published=True)
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
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = POSTS_PER_PAGE
    queryset = Post.objects.select_related(
        'category').filter(
                is_published=True,
                pub_date__lte=current_datetime,
                category__is_published=True).annotate(
                    comment_count=Count('comments')
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user}
                       )


class PostUpdateDeleteMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(PostUpdateDeleteMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(PostUpdateDeleteMixin, DeleteView):
    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user}
                       )


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.current_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']}
                       )


class CommentUpdateDeleteMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        return get_object_or_404(
            Comment,
            author=self.request.user,
            post_id=self.kwargs['post_id'],
            id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']}
                       )


class CommentUpdateView(CommentUpdateDeleteMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentUpdateDeleteMixin, DeleteView):
    pass
