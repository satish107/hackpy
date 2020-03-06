# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AddUserForm

# Create your views here.

def signup(request):
	if request.method == 'POST':
		sign_up_form = AddUserForm(request.POST)
		if sign_up_form.is_valid():
			sign_up_form.save(commit = False)
			username = sign_up_form.cleaned_data.get('username')
			email = sign_up_form.cleaned_data.get('email')
			password1 = sign_up_form.cleaned_data.get('password1')
			password2 = sign_up_form.cleaned_data.get('password2')
			user = sign_up_form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			return redirect('/')
	else:
		sign_up_form = AddUserForm()
		print(sign_up_form)
	return render(request, 'users/signup.jinja', {'sign_up_form': sign_up_form})


def login_user(request):
	if request.method == 'POST':
		form = AuthenticationForm(data = request.POST)
		print(form)
		if form.is_valid():
			email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(email = email, password = password)
			login(request, user)
			return redirect('/')
	else:
		form = AuthenticationForm()
		print(form)
	return render(request, 'users/login.jinja', {'form': form})


@login_required
def logout_user(request):
	logout(request)
	return redirect('/')
	
