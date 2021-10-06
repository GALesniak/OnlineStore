from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import random


class WelcomeView(View):
    login_url = 'account:login'

    def get(self, request):
        return render(request, 'account/index.html')


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        str_num = str(random.randrange(1223, 9999))
        request.session['cap'] = str_num
        return render(request, 'account/login.html', {'cap': str_num})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            cap = request.POST.get('cap')
            user = authenticate(request, username=username, password=password)
            if str(cap) == request.session.get('cap'):
                pass
            else:
                messages.info(request, 'Verification Code is incorrect')
                return render(request, 'account/login.html')
            if user is not None:
                login(request, user)
                return redirect('account:index')
            else:
                messages.info(request, 'Username or Password is incorrect')
            return render(request, 'account/login.html')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('onlineshop:product_list')


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'account/registration.html', {'form': form})

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be at least 6 characters long')
            return redirect('account:register')
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords do not match')
            return redirect('register')

        if '@' and '.' not in email:
            messages.add_message(request, messages.ERROR,
                                 'Please provide a valid email')
            return redirect('account:register')

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken')

        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                return redirect('account:register')


        except Exception as identifier:
            pass

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Your account has been created!')
        return redirect('account:login')
