from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, View, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser, VerificationCode
from .forms import UserRegisterForm, VerificationForm, CustomUserChangeForm
from django.contrib.auth import login, logout
from .mixins import NoAuthenticatedAccessMixin
from django.contrib import messages
from .utils import send_verification_email

class UserLoginView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        verification_code = VerificationCode(user=user, email=user.email)
        verification_code.save()
        send_verification_email(user.email, verification_code.code)
        self.request.session['pending_user_id'] = user.id
        self.request.session['verification_type'] = 'login'
        self.request.session.modified = True
        self.request.session.save()
        messages.info(self.request, 'A verification code has been sent to your email.')
        return redirect('account:verify')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['username'].widget.attrs.update({
            'class': 'form-control ',
        })
        context['form'].fields['password'].widget.attrs.update({
            'class': 'form-control',
        })
        return context

    def get_success_url(self):
        return reverse_lazy('account:verify')


class UserRegisterView(NoAuthenticatedAccessMixin, CreateView):
    template_name = 'account/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save()
        verification_code = VerificationCode(user=user, email=user.email)
        verification_code.save()
        send_verification_email(user.email, verification_code.code)
        self.request.session['pending_user_id'] = user.id
        self.request.session['verification_type'] = 'register'
        self.request.session.modified = True
        self.request.session.save()
        messages.info(self.request, 'A verification code has been sent to your email.')
        return redirect('account:verify')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home:index')


class VerificationCodeView(NoAuthenticatedAccessMixin, View):
    template_name = 'account/verify.html'
    form_class = VerificationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            verification_type = request.session.get('verification_type')
            pending_user_id = request.session.get('pending_user_id')

            if not verification_type or not pending_user_id:
                messages.error(request, 'Invalid verification session.')
                return redirect('account:login')

            try:
                user = CustomUser.objects.get(id=pending_user_id)
                verification_code = VerificationCode.objects.filter(email=user.email, code=code).latest('created_at')
                if verification_code.is_valid():
                    if verification_type == 'register':
                        user.is_verified = True
                        user.save()
                        login(request, user)
                    elif verification_type == 'login':
                        login(request, user)

                    verification_code.delete()
                    request.session.modified = True
                    request.session.save()
                    return redirect('home:index')
                else:
                    messages.error(request, 'Verification code has expired.')
            except VerificationCode.DoesNotExist:
                messages.error(request, 'Invalid verification code.')
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user

class UserProfileUpdatedView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user

