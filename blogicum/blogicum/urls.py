from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

handler403 = 'core.views.csrf_failure'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = [
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:profile'),
        ),
        name='registration',
    ),
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
