from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Category, Post
from .mixins import (SuccessUrlToPostMixin,
                     SuccessUrlToProfileMixin,
                     PostFormMixin,
                     PostFormValidMixin,
                     PostRequiredAttrsMixin,
                     PostUpdateDeleteMixin,
                     CommentFormMixin,
                     CommentRequiredAttrsMixin,
                     CommentUpdateDeleteMixin)
from .forms import CommentForm, ProfileForm

POSTS_PER_PAGE = 10
User = get_user_model()


def paginate(queryset, request):
    '''Returns a page object.'''

    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def annotate_comment_count(queryset):
    '''Adds annotations about the number of comments to the post.'''

    return queryset.annotate(comment_count=Count('comments')).order_by(
                '-pub_date')


def get_posts_qs_by_category():
    return annotate_comment_count(Post.objects.select_related(
        'category').filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True))


def get_posts_gs_by_author(username):
    return annotate_comment_count(Post.objects.select_related(
        'author').filter(
            author__username=username))


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


class ProfileUpdateView(LoginRequiredMixin,
                        SuccessUrlToProfileMixin,
                        UpdateView):
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user


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
                     PostRequiredAttrsMixin,
                     PostFormValidMixin,
                     PostFormMixin,
                     CreateView):
    pass


class PostUpdateView(PostUpdateDeleteMixin,
                     PostFormMixin,
                     UpdateView):
    pass


class PostDeleteView(PostUpdateDeleteMixin,
                     SuccessUrlToProfileMixin,
                     DeleteView):
    pass


class CommentCreateView(LoginRequiredMixin,
                        SuccessUrlToPostMixin,
                        CommentRequiredAttrsMixin,
                        PostFormValidMixin,
                        CommentFormMixin,
                        CreateView):

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.current_post
        return super().form_valid(form)


class CommentUpdateView(CommentUpdateDeleteMixin,
                        CommentFormMixin,
                        UpdateView):
    pass


class CommentDeleteView(CommentUpdateDeleteMixin, DeleteView):
    pass
