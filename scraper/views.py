from typing import final
from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
# Create your views here.
from .models import Search


BASE_CRAIGLIST_URL = 'https://indore.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://image.craigslist.org/{}_300x300.jpg'
def home(request):
    print('Welcome Home')
    return render(request, 'scraper/base.html')
    

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search = search)
    # final_url = BASE_CRAIGLIST_URL
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data,features='html.parser')
    post_listings = soup.find_all('li',{'class':'result-row'})



    final_postings = []
    for post in post_listings :
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if (post.find(class_='result-price')):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            search = post_image_url
        else :
            post_image_url = 'https://craigslist.org/images/peace.jpg'
            search = post_image_url



        final_postings.append((post_title, post_url, post_price, post_image_url))
        
    # print(final_url)
    # print(quote_plus(search))
    stuff_for_frontend = {
        'search' : f'{search}',
        'final_postings' : final_postings,
    }
    return render(request,'scraper/search.html',stuff_for_frontend  )