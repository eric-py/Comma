from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

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