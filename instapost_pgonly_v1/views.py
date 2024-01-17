"""
To render html web pages
"""
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from posts.models import Post

def home_view(request, *args, **kwargs):
    posts = Post.objects.all()
    return render(request, 'home-view.html', {'posts': posts})
