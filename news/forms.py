# -*- coding: utf-8 -*-
from django import forms
from .models import News, Comment

class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = ['title', 'link', 'text']


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']