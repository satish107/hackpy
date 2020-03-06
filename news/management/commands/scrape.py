# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json
import re

from news.models import News, Comment
from django.contrib.auth.models import User
from users.models import UserProfile
import random
import string


def random_email(email_prefix_length = 10):
	prefix = string.ascii_lowercase
	email_prefix = ''.join(random.choice(prefix) for i in range(email_prefix_length))
	return email_prefix + '@gmail.com'



class Command(BaseCommand):
	help = "collect news"
	base_url = 'https://news.ycombinator.com/'
	counter = 1000
	def handle(self, *args, **kwargs):
		page = requests.get(self.base_url)
		soup = BeautifulSoup(page.content, 'html.parser')
		news_ids = soup.find_all('tr', class_ = 'athing')
		next_link = soup.find('a', class_ = 'morelink')
		hn_users = soup.find_all('a', class_ = 'hnuser')
		new_url = self.base_url[:29] + next_link['href']
		self.base_url = new_url
		for (i, h) in zip(news_ids, hn_users):
			news_id = 'item?id=' + i['id']
			news_url_with_id = 'https://news.ycombinator.com/' + news_id
			title = i.contents[4].a.string
			link = i.contents[4].a['href']
			hn_user = h.string
			hn_user_email = '%s%s@gmail.com' %(random_email, hn_user)

			# If user exists -> get user -> create comment
			# If user not exists -> create user -> create comment

			if UserProfile.objects.filter(username=hn_user).exists():
				user = UserProfile.objects.filter(username=hn_user).last()
			else:
				user = UserProfile.objects.create(username = hn_user, email = random_email())
				user.set_password('hn@password')
				user.save()

			if not News.objects.filter(title = title).exists():
				news = News.objects.create(title = title, link = link, user = user)
				news.weight = self.counter
				news.save()
				self.counter += 1
				comment_page = requests.get(news_url_with_id)
				comment_soup = BeautifulSoup(comment_page.content, 'html.parser')
				comments = comment_soup.find_all('td', class_ = 'default')
				
				for comment in comments:
					hn_user = comment.find('a', {'class': 'hnuser'}).string

					if UserProfile.objects.filter(username=hn_user).exists():
						user = UserProfile.objects.filter(username=hn_user).last()
					else:
						user = UserProfile.objects.create(username = hn_user, email = random_email())
						user.set_password('hn@password')
						user.save()
					
					comment_text = comment.find('div', {'class': 'comment'}).text
					if not Comment.objects.filter(text=comment_text):
						comment = Comment.objects.create(user= user, news = news, text=comment_text)
		self.handle()
				




