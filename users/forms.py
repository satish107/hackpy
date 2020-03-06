# -*- coding: utf-8 -*-
from django import forms
from .models import UserProfile

class AddUserForm(forms.ModelForm):
	password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
	password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ['username', 'email']

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('password doesnot match')
		return password2

	def save(self, commit = True):
		user = super(AddUserForm, self).save(commit = False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
