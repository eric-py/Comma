from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from posts.models import Post

class UserSpecificActionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if 'username' in kwargs:
            if request.user.username != kwargs['username']:
                return redirect(reverse('account:profile', kwargs={'username': request.user.username}))
        
        elif 'pk' in kwargs:
            obj = self.get_object()
            if obj.user != request.user:
                return redirect(reverse('account:profile', kwargs={'username': request.user.username}))
        
        return super().dispatch(request, *args, **kwargs)

class AnonymousRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('posts:home')

class PostVisibilityMixin(UserPassesTestMixin):
    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        user = self.request.user
        
        if post.user == user:
            return True
        
        if not post.user.is_private:
            return True
        
        if post.user.followers.filter(follower=user).exists():
            return True
        
        return False