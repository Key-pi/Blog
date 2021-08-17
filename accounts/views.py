from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DetailView
from django.shortcuts import get_object_or_404

import requests

from boards.models import Blogger, Reader
from .forms import BloggerRegisterForm, ReaderRegisterForm, SignUpForm, ReaderUpdate, BloggerUpdate
from .tasks import send_email_task


def signup(request):
    return render(request, 'choose_role.html')


def signup_blogger(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        form_user = SignUpForm(request.POST)
        form_blogger = BloggerRegisterForm(request.POST)

        if form_user.is_valid() and form_blogger.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                user = form_user.save()
                country = form_blogger.cleaned_data['country']
                city = form_blogger.cleaned_data['city']
                Blogger.objects.create(user=user,country=country, city=city)

                messages.add_message(request, messages.SUCCESS, 'Congratulations, you have successfully registered.')

                if user is not None:
                    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    send_email_task.delay(user.email)
                    return redirect('boards:home')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'signup_blogger.html', context={'form': form_user, 'form1': form_blogger})

        else:

            return render(request, 'signup_blogger.html', context={'form': form_user, 'form1': form_blogger})

    else:
        form_user = SignUpForm()
        form_blogger = BloggerRegisterForm()

        return render(request, 'signup_blogger.html', context={'form': form_user, 'form1': form_blogger})


def signup_reader(request,  backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":

        form_user = SignUpForm(request.POST)
        form_reader = ReaderRegisterForm(request.POST)

        if form_user.is_valid() and form_reader.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                user = form_user.save()
                adult = form_reader.cleaned_data['adult']
                Reader.objects.create(user=user, adult=adult)
                messages.add_message(request, messages.SUCCESS, "Congratulations, you have successfully registered.")

                if user is not None:
                    auth.login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
                    send_email_task.delay(user.email)
                    return redirect('boards:home')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'signup_reader.html', context={'form': form_user, 'form1': form_reader})
        else:
            return render(request, 'signup_reader.html', context={'form': form_user, 'form1': form_reader})
    else:
        form_user = SignUpForm()
        form_reader = ReaderRegisterForm()
        return render(request, 'signup_reader.html', context={'form': form_user, 'form1': form_reader})


class Login(LoginView):
    model = User
    template_name = 'login.html'

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(self.request, user)
                return redirect('boards:home')
            else:
                messages.error(self.request, 'Incorrect username or password. Please try again.')
                return render(self.request, 'login.html', {'form': form})
        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return render(self.request, 'login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    template_name = 'my_account.html'
    # exclude =('avatar',)
    success_url = reverse_lazy('accounts:my_account')
    def get_form_class(self):
        try:
            if self.request.user.blogger_user.is_super_user:
                self.form_class = BloggerUpdate
        except:
            self.form_class = ReaderUpdate
        return self.form_class

    def get_object(self, queryset=None):
        try:
            return Blogger.objects.get(user=self.request.user)
        except :
            return Reader.objects.get(user=self.request.user)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.add_message(self.request,messages.SUCCESS,'account has been updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)




class DetailProfile(DetailView):
    model = User
    template_name = 'detail_profile.html'
    context_object_name = 'profile_user'



# def detail_profile(request, pk):
#     if request.method == "POST":
#         user = User.objects.get_object_or_404(pk=pk)
#         return render(request, 'detail_profile.html', context={'profile_user': user})
#






#
# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(SuccessMessageMixin, UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email', )
#     template_name = 'my_account.html'
#     success_message = 'Account successfully updated!)'
#     success_url = reverse_lazy('accounts:my_account')
#
#     def get_object(self, queryset=None):
#         return self.request.user