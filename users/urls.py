from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, VerificationTemplateView, generate_new_password, \
    ErrorVerificationTemplateView, ProfileDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/confirm_delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile_confirm_delete'),

    path('verify_email/', VerificationTemplateView.as_view(), name='verify_email'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('verify_email/error/', ErrorVerificationTemplateView.as_view(), name='verify_email_error'),
]
