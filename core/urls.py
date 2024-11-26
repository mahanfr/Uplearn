from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('pages.urls'))
]

urlpatterns += i18n_patterns(
    path('', include('pages.urls')),
    path('register', account_views.register_view, name="register"),
    path('login', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout")
)
