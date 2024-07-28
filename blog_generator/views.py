from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import BlogPost
import os
import json
from pytube import YouTube
# import assemblyai as aai
# import openai


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)


        # get yt title
        title, views, publish_date  = yt_title(yt_link)


        # save blog article to database
        new_blog_article = BlogPost.objects.create(
            user = request.user,
            youtube_title = title,
            youtube_link = yt_link,
            views = views,
            publish_date = publish_date,
        )
        new_blog_article.save()

        # return blog article as a response
        return JsonResponse({'content': title})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    views = yt.views
    publish_date = yt.publish_date

    return title, views , publish_date

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user = request.user)
    return render(request, 'all-blogs.html', {'blog_articles':blog_articles})

def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user  == blog_article_detail.user:
        return render(request, 'blog-details.html', {'blog_article_detail':blog_article_detail})
    else:
        return redirect('/')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']

        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user) 
            return redirect('/')
        else:
            error_message = "Invalid Username or Password" 
            return render(request, 'login.html', {'error_message':error_message})       
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email =  request.POST['email']
        password =  request.POST['password']
        repeatpassword =  request.POST['repeatpassword']

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error Creating account'
                return render(request, 'signup.html', {'error_message':error_message})

        else:
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message':error_message})
        
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')