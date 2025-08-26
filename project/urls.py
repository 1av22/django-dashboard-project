
from django.contrib import admin
from django.urls import path, include
from dashboard.views import DashboardView, SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('dashboard.urls')),
    path('', DashboardView.as_view(), name='dashboard'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    path('signup/', SignUpView.as_view(), name='signup')

]
