from django.shortcuts import render
from django.views.generic import ListView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Post, Like, SavedPost
from .forms import PostForm

# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        return Post.objects.posts(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | صفحه اصلی'
        context['active'] = 'home'
        [setattr(post, 'is_liked', post.likes.filter(user=self.request.user).exists()) for post in context['posts']]
        [setattr(post, 'is_saved', post.saves.filter(user=self.request.user).exists()) for post in context['posts']]
        return context

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post:
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                like.delete()
                liked = False
            else:
                liked = True
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes_count': post.likes.count()
        })

class SavePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
        if not created:
            saved_post.delete()
            saved = False
        else:
            saved = True
        return JsonResponse({
            'status': 'success',
            'saved': saved,
        })

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | افزودن پست'
        context['active'] = 'create'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

