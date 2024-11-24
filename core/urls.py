from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('pages.urls'))
]

urlpatterns += i18n_patterns(
    path('', include('pages.urls')),
    path('register', account_views.register_view),
)
