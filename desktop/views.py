from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView

from .utilities import signer
from .forms import ChangeUserInfoForm, RegisterUserForm
from .models import AdvUser


def index(request):
    return render(request, 'basic.html')


class BBLoginView(LoginView):
    template_name = 'desktop/login.html'

@login_required
def profile(request):
    return render(request, 'desktop/profile.html')

class DTLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'desktop/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'desktop/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('desktop:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'desktop/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('desktop:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'desktop/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'desktop/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'desktop/user_is_activated.html'
    else:
        template = 'desktop/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)