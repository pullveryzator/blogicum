from django.urls import path

from . import views

app_name = 'blog'

# urlpatterns = [
#     path('', views.PostListView.as_view(), name='index'),
#     path('category/<slug:category_slug>/', views.category_posts,
#          name='category_posts'),
#     path('profile/<username>/', views.profile, name='profile'),
#     path('posts/<int:id>/', views.post_detail, name='post_detail'),
# ]


urlpatterns = [
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('', views.PostListView.as_view(), name='index'),
    path('profile/<username>/', views.profile, name='profile'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='posts_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='posts_delete'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
]
