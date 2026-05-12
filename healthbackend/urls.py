from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from core.views import CustomGraphQLView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('*', TemplateView.as_view(template_name="not-found.html"), name="not-found"),
    path('admin/', admin.site.urls),
    path('graphql/', CustomGraphQLView.as_view(graphiql=True), name="graphql"),
    path('api/', include('core.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)