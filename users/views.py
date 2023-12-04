import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Подтверждение почты',
                message=f'Код {new_user.ver_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


# Верификация пользователя, проверка на корректность введенного кода
class VerificationTemplateView(TemplateView):
    template_name = 'users/verify_email.html'

    def post(self, request):
        ver_code = request.POST.get('ver_code')
        user_code = User.objects.filter(ver_code=ver_code).first()

        if user_code is not None and user_code.ver_code == ver_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verify_email_error')


# Контроллер, для отображения страницы, при неправильном вводе кода, при верификации почты
class ErrorVerificationTemplateView(TemplateView):
    template_name = 'users/verify_email_error.html'
    success_url = reverse_lazy('users:verify_email_error')


# Контроллер для отображения профиля пользователя на основе UpdateView (возможность изменения данных)
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:home')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


# Функция отвечает за генерацию пароля и его отправку на почту
def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))
