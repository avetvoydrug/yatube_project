from django.http import JsonResponse
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from django.urls import reverse_lazy


from django.shortcuts import redirect
from .models import Post, Group, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm
from django.views.decorators.cache import cache_page


User = get_user_model()

@cache_page(20)
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Main PAge'
    context = {
        'page_obj': page_obj,
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
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group' : group,
        'page_obj' : page_obj,
    }
    # title = 'Записи сообщества'
    # text = 'Здесь будет информация о группах проекта Yatube'
    # context = {
    #     'title': title,
    #     'text' : text
    # }
    return render(request, template, context)
# Create your views here.

def profile(request, username):
    #some = User.objects.get(username=username)
    some = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=some).order_by('-pub_date')
    cnt = Post.objects.filter(author=some).count()
    author = some.get_full_name()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Профиль пользователя {username}'
    context = {
        'page_obj' : page_obj,
        'title' : title,
        'cnt': cnt,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    comments = Comment.objects.filter(post=post)
    cnt = Post.objects.filter(author=author).count()
    title = str(post.text)[:30]
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'cnt': cnt,
        'title': title,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    # if request.method == 'POST':
    group_list = Group.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        post_create = form.save(commit=False)
        post_create.author = request.user
        # text = form.cleaned_data['text']
        # group = form.cleaned_data['group']
        # form.save()
        post_create.save()
        return redirect(f'/profile/{request.user}/')

    return render(
        request, 
        'posts/post_create.html', 
        {
            'form': form,
            'group_list': group_list
        }
    )

def post_edit(request, post_id):
    # post = get_object_or_404(Post, pk=post_id)
    is_edit = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST, 
        files=request.FILES or None,
        instance=is_edit
    )
    if is_edit.author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method != 'POST' or not form.is_valid():
        form = PostForm(instance=is_edit)
        return render(
            request,
            'posts/post_create.html',
            {
                'form': form,
                'post_id': post_id,
                'is_edit': is_edit
            }
        )

    form.save()
    return redirect('posts:post_detail', post_id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
    
#### ______ API.VIEWS ______ ####
@api_view(['GET', 'POST'])
def api_posts(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    if request.user != post.author:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == ('PUT' or 'PATCH'):
        serializer = PostSerializer(post, data=request.data, partial=True,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#class APIPostList(generics.ListCreateAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer

#class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Post.objects.all()
#    serializer_class = PostSerializer