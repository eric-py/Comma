from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Post, Like, SavedPost, Comment
from .forms import PostForm

from extensions.mixins import UserSpecificActionMixin, PostVisibilityMixin
from extensions.utils import create_comment_or_reply

User = get_user_model()

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

class PostDetailView(LoginRequiredMixin, PostVisibilityMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['title'] = "Comma | نمایش پست"
        context['active'] = 'home'
        context['is_liked'] = post.likes.filter(user=self.request.user).exists()
        context['is_saved'] = SavedPost.objects.filter(user=self.request.user, post=post).exists()
        context['comments'] = post.comments.filter(parent=None)
        return context

class PostDeleteView(UserSpecificActionMixin, DeleteView):
    model = Post
    
    def get_success_url(self):
        return reverse('account:profile', kwargs={'username': self.request.user.username})

class PostEditView(UserSpecificActionMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('posts:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | ویرایش پست'
        context['active'] = 'edit'
        return context

class SearchView(LoginRequiredMixin, ListView):
    template_name = 'posts/post_search.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            posts = Post.objects.filter(
                Q(caption__icontains=query)
            )
            results = list(users) + list(posts)
            return results
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        context['title'] = 'Comma | جستجو'
        context['active'] ='search'
        
        # Separate users and posts for the template
        context['users'] = [item for item in context['results'] if isinstance(item, User)]
        context['posts'] = [item for item in context['results'] if isinstance(item, Post)]
        
        return context

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        
        if not content:
            return JsonResponse({'status': 'error', 'message': 'داده‌های نامعتبر'})
        
        try:
            comment = create_comment_or_reply(post, request.user, content)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
        return JsonResponse({
            'status': 'success',
            'username': comment.user.username,
            'user_profile_pic': comment.user.profile_pics.url if comment.user.profile_pics else '',
            'text': comment.text,
            'created_at': comment.jcreated_at()
        })

class AddReplyView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        parent_id = request.POST.get('parent_id')
        content = request.POST.get('content')

        if not (parent_id and content):
            return JsonResponse({'status': 'error', 'message': 'داده‌های نامعتبر'})

        parent_comment = get_object_or_404(Comment, id=parent_id)
        
        try:
            reply = create_comment_or_reply(post, request.user, content, parent_comment)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
        return JsonResponse({
            'status': 'success',
            'username': reply.user.username,
            'user_profile_pic': reply.user.profile_pics.url if reply.user.profile_pics else '',
            'text': reply.text,
            'created_at': reply.jcreated_at()
        })

class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes_count': comment.like_count()
        })