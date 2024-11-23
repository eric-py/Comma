from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .forms import CustomUserCreationForm
from .models import UserConnection, FollowRequest
from .mixins import AnonymousRequiredMixin

from posts.models import SavedPost

User = get_user_model()

# Create your views here.

class UserLoginView(AnonymousRequiredMixin, LoginView):
    template_name = 'account/auth.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | صفحه ورود'
        context['active'] = 'login'
        return context

class UserRegisterView(AnonymousRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'account/auth.html'
    success_url = reverse_lazy('account:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | ثبت نام'
        context['active'] = 'register'
        return context

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_following = UserConnection.objects.filter(follower=self.request.user, following=self.object).exists()
        is_requested = FollowRequest.objects.filter(from_user=self.request.user, to_user=self.object).exists()
        context['is_following'] = is_following
        context['is_requested'] = is_requested
        context['saved_posts'] = SavedPost.objects.saved_posts(self.object)
        context['title'] = f'Comma | پروفایل {self.object.username}'
        context['active'] = 'profile'
        return context

class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        user = request.user

        if user == user_to_follow:
            return JsonResponse({'status': 'error', 'message': 'شما نمیتوانید خودتان را فالوو کنید.'})

        follow_request = FollowRequest.objects.filter(from_user=user, to_user=user_to_follow).first()
        connection = UserConnection.objects.filter(follower=user, following=user_to_follow).first()

        if user_to_follow.is_private:
            if follow_request:
                follow_request.delete()
                return JsonResponse({'status': 'success', 'action': 'request_cancelled'})
            elif connection:
                connection.delete()
                return JsonResponse({'status': 'success', 'action': 'unfollowed'})
            else:
                FollowRequest.objects.create(from_user=user, to_user=user_to_follow)
                return JsonResponse({'status': 'success', 'action': 'request_sent'})
        else:
            if connection:
                connection.delete()
                return JsonResponse({'status': 'success', 'action': 'unfollowed'})
            else:
                UserConnection.objects.create(follower=user, following=user_to_follow)
                return JsonResponse({'status': 'success', 'action': 'followed'})