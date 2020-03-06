# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

# Create your models here.

class News(models.Model):
	title = models.CharField(max_length = 255)
	link = models.URLField(max_length = 200)
	text = models.TextField(null = True, blank = True)
	user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
	created = models.DateTimeField(auto_now_add = True)
	weight = models.IntegerField(null = True, blank = True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
	news = models.ForeignKey(News, on_delete = models.CASCADE, related_name = 'comments')
	text = models.TextField()
	reply = models.ForeignKey('self', null = True, blank = True)
	created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.text