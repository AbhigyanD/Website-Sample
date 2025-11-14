from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError('This password is too short. It must contain at least 8 characters')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError({'password2': 'The two password fields didn\'t match'})

        return cleaned_data


def register_view(request):
    if request.method == 'POST':
        # Handle missing fields gracefully - treat as empty strings
        post_data = request.POST.copy()
        for field in ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']:
            if field not in post_data:
                post_data[field] = ''
        
        form = RegisterForm(post_data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data.get('email', '')
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            return redirect('/accounts/login/')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'accounts/login.html', {
                'error': 'Username or password is invalid',
                'username': username
            })

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/accounts/profile/view/')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Username or password is invalid',
                'username': username
            })
    else:
        return render(request, 'accounts/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/accounts/login/')

