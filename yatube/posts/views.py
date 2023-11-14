from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from django.template import loader

from .models import Post, Group

def index(request):
    # Адрес шаблона сохраним в переменную, это не обязательно, но удобно
    #template = 'posts/index.html'
    # Строку, которую надо вывести на страницу, тоже сохраним в переменную
    #title = 'Последние обновления сайта'
    # Словарь с данными принято называть context
    posts = Post.objects.order_by('-pub_date')[:10]
    title = 'Main PAge'
    context = {
        'posts' : posts,
        'title' : title
    }
    # context = {
    #     'title' : title,
    #     'text' : 'Это ГЛАВНАЯ страница проекта Yatube'
    # }
    # Третьим параметром передаём словарь context
    return render(request, 'posts/index.html', context)
    #return render(request, template, context)

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group' : group,
        'posts' : posts,
    }
    # title = 'Записи сообщества'
    # text = 'Здесь будет информация о группах проекта Yatube'
    # context = {
    #     'title': title,
    #     'text' : text
    # }
    return render(request, template, context)
# Create your views here.
