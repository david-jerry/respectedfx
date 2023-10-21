from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'objects'
    paginate_by = 10  # Adjust the number of posts per page as needed

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'object'

# Create your views here.
