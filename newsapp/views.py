"""newsapp View"""
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render

from .forms import \
    LoginForm  # Assuming you have a form named LoginForm in forms.py
from .forms import RegistrationForm
from .models import UserSearch

API_KEY = "c3c9a565056c49e6923348aea449ff6d"

@login_required(login_url='login')
def fetch_news(request):
    articles = []
    keyword = ""

    # (POST request)
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': keyword,
            'sortBy': 'popularity',
            'apiKey': API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()
        articles = data.get('articles', [])

        # Format the date for each article
        for article in articles:
            dt = datetime.strptime(
                article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            article['publishedAtFormatted'] = dt.strftime('%Y-%m-%d %H:%M:%S')

        # Save the user's search query to the database
        if request.user.is_authenticated:
            UserSearch.objects.create(user=request.user, keyword=keyword)

    recent_searches = UserSearch.objects.order_by(
        '-searched_at')[:10]  # gets the last 10 searches

    return render(request, 'Search_news.html', {
        'articles': articles,
        'keyword': keyword,
        'recent_searches': recent_searches
    })

# fetch news only simple
# API_ENDPOINT = "https://newsapi.org"
# API_ENDPOINT = "https://newsapi.org"
# API_KEY = "c3c9a565056c49e6923348aea449ff6d"

# def fetch_news(request):
#     articles = []
#     keyword = ""

#     # (POST request)
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword', '')
#         url = 'https://newsapi.org/v2/everything'
#         params = {
#             'q': keyword,
#             'sortBy': 'popularity',
#             'apiKey': API_KEY
#         }

#         response = requests.get(url, params=params)
#         data = response.json()
#         articles = data.get('articles', [])

#         # Format the date for each article
#         for article in articles:
#             dt = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
#             article['publishedAtFormatted'] = dt.strftime('%Y-%m-%d %H:%M:%S')

#         # Save the user's search query to the database
#         if request.user.is_authenticated:
#             UserSearch.objects.create(user=request.user, query=keyword)

#     return render(request, 'Search_news.html', {'articles': articles, 'keyword': keyword})


# ------------------------------------------------------------------------------------------
API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'

@login_required(login_url='login')
def headlines(request):
    keyword = request.GET.get('keyword', '')
    sort_by = request.GET.get('sort_by', 'popularity')
    articles = []

    params = {'country': 'in', 'apiKey': API_KEY, 'sortBy': sort_by}
    if keyword:
        params['q'] = keyword

    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        for article in articles:
            dt = datetime.strptime(
                article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            article['publishedAtFormatted'] = dt.strftime('%Y-%m-%d %H:%M:%S')

    paginator = Paginator(articles, 10)  # Show 10 articles per page

    page = request.GET.get('page')
    try:
        articles_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        articles_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results.
        articles_page = paginator.page(paginator.num_pages)

    context = {
        'keyword': keyword,
        'articles': articles_page,
    }

    return render(request, 'headlines.html', context)


# API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'

# def headlines(request):
#     keyword = request.GET.get('keyword', '')
#     sort_by = request.GET.get('sort_by', 'popularity')
#     articles = []

#     params = {'country': 'in', 'apiKey': API_KEY, 'sortBy': sort_by}
#     if keyword:
#         params['q'] = keyword

#     response = requests.get(API_ENDPOINT, params=params)
#     data = response.json()

#     if data['status'] == 'ok':
#         articles = data['articles']
#         for article in articles:
#             dt = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
#             article['publishedAtFormatted'] = dt.strftime('%Y-%m-%d %H:%M:%S')

#         # Sort the articles by date (newest first) before passing them to the paginator
#         articles.sort(key=lambda x: x['publishedAt'], reverse=True)

#     paginator = Paginator(articles, 10)  # Show 10 articles per page

#     page = request.GET.get('page')
#     try:
#         articles_page = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver the first page.
#         articles_page = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range, deliver the last page of results.
#         articles_page = paginator.page(paginator.num_pages)

#     context = {
#         'keyword': keyword,
#         'articles': articles_page,
#     }

#     return render(request, 'headlines.html', context)


# ------------------------------------------------------------------------------------------
SOURCES_ENDPOINT = 'https://newsapi.org/v2/top-headlines/sources'

@login_required(login_url='login')
def sources(request):
    response = requests.get(SOURCES_ENDPOINT, params={'apiKey': API_KEY})
    data = response.json()
    sources = data.get('sources', [])

    context = {
        'sources': sources,
    }

    return render(request, 'sources.html', context)

# ------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
@login_required(login_url='login')
def home2(request):
    return render(request,"home.html")
