import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        link = f"http://{host}/users/confirm-register/{token}"
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке: {link}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

    def confirm_email(request, token):
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.save()

        return redirect(reverse("users:login"))
