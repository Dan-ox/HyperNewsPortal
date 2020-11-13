from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.conf import settings
import json
import time
import random


# Create your views here.
# C:/Users/Daniyar/PycharmProjects/HyperNews Portal1/HyperNews Portal/task/hypernews/news/news.json

with open(settings.NEWS_JSON_PATH, 'r') as json_file:
    news_dict = json.load(json_file)

# with open("C:/Users/Daniyar/PycharmProjects/HyperNews Portal1/HyperNews Portal/task/hypernews/news/news.json", 'r') \
#         as json_file:
#     news_dict = json.load(json_file)


def home_view(request):
    # return render(request, 'news/home_view.html')
    return redirect('/news/')


def get_context(link):
    for i in news_dict:
        if link in i.values():
            return i


class NewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        news = get_context(news_id)
        if not news:
            raise Http404
        context = {"news": news}
        return render(request, "news/index.html", context=context)


def sort_post():
    pre_sorted = sorted(news_dict, key=lambda i: i['created'], reverse=True)
    sorted_news = {}
    for i in pre_sorted:
        date = i['created'][:10]
        if date not in sorted_news:
            sorted_news[date] = [i]
        else:
            sorted_news[date].append(i)

    return sorted_news


def find_news(title):
    news_list = sort_post()
    found_news = {}
    for date in news_list:
        for dic in news_list[date]:
            if title in dic['title']:

                if date not in found_news:
                    found_news[date] = [dic]
                else:
                    found_news[date].append(dic)
    return found_news


class MainPage(View):
    def get(self, request):
        title = request.GET.get('q')
        if title:
            context = {"news": find_news(title)}
        else:
            context = {"news": sort_post()}
        # return render(request, 'news/found_news.html', context=context)

        return render(request, 'news/main.html', context=context)


class CreateNews(View):
    news_dict_updated = news_dict
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        # created = datetime.now()
        created = time.strftime("%Y-%m-%d %H:%M:%S")
        link = random.randint(0,9999999)
        created_news = {'created': created, 'text': text, 'title': title, 'link': link}

        self.news_dict_updated.append(created_news)
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json.dump(self.news_dict_updated, json_file, indent=2)

        return redirect('/news/')

    def get(self, request, *args, **kwargs):
        return render(request, 'news/Create_news.html')


# print(find_news("W"))
