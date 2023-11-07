from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse('Main page',
                        'Your advertisement could be here...')

def group_posts(request, group_name):
    return HttpResponse(f'This group was made by: {group_name}')
# Create your views here.
