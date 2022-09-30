import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
# Create your views here.


BASE_ANIME_URL = 'https://chia-anime.su/?s={}'


def index(request):
	return render(request, 'index.html')

def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search)
	final_url = BASE_ANIME_URL.format(quote_plus(search))
	response = requests.get(final_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')
	posts = soup.find_all('article', {'class': 'bs'})

	final_post = [] 

	for post in posts:
		 post_title = post.find('h2').text 
		 post_url = post.find('a').get('href')
		 post_status = post.find(class_='epx').text
		 post_image_url = post.find('img').get('src')


		 final_post.append((post_title,post_url,post_status, post_image_url)) 



	frondend_result = {
	'search':search,
	'final_post': final_post,
	}


	return render(request, 'theapp/new_search.html', frondend_result)