from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django import forms
from django.core.exceptions import ValidationError


def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email or '',
        'first_name': user.first_name or '',
        'last_name': user.last_name or ''
    })


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1:
            if password1 != password2:
                raise forms.ValidationError({'password2': 'The two password fields didn\'t match'})
            if len(password1) < 8:
                raise forms.ValidationError({'password1': 'This password is too short. It must contain at least 8 characters'})

        return cleaned_data


def profile_edit_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')

            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)

            user.save()
            return redirect('/accounts/profile/view/')
    else:
        form = ProfileEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

    return render(request, 'accounts/profile_edit.html', {'form': form})

