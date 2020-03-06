# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.

def all_news(request):
	all_news = News.objects.all().order_by('weight')
	page = request.GET.get('page', 1)
	paginator = Paginator(all_news, 30)
	try:
		page_news = paginator.page(page)
	except PageNotAnInteger:
		page_news = paginator.page(1)
	except EmptyPage:
		page_news = paginator.page(paginator.num_pages)

	context = {
		'all_news': all_news,
		'page_news': page_news,
	}
	return render(request, 'news/home.jinja', context)

def news(request, id):
	news = get_object_or_404(News, id = id)
	news_all_comemnts = news.comments.all().order_by('-created')
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit = False)
			if request.user.is_authenticated():
				new_comment.user = request.user
				new_comment.news = news
				new_comment.save()
				return redirect(request.path_info)
			return redirect('/users/login')
	else:
		comment_form = CommentForm()
	context = {
		'news': news,
		'comment_form': comment_form,
		'all_comments': news_all_comemnts
	}
	return render(request, 'news/news_detail.jinja', context)


counter = 1
@login_required(login_url = "/users/login")
def create_news(request):
	if request.method == 'POST':
		form = NewsForm(request.POST)
		if form.is_valid():
			news = form.save(commit = False)
			news.user = request.user
			global counter
			news.weight = counter
			news.save()
			counter += 1
			return redirect('/')
	else:
		form = NewsForm()
	return render(request, 'news/create_news.jinja', {'form': form})


def search(request):
	query = request.GET.get('q')
	searched_items = News.objects.filter(Q(title__icontains = query)).order_by('-created')
	context = {
		'searched_items': searched_items
	}
	return render(request, 'news/search.jinja', context)




