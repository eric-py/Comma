from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, View, UpdateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth import views

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserConnection, FollowRequest, Activity

from posts.models import SavedPost

from extensions.mixins import UserSpecificActionMixin, AnonymousRequiredMixin, FollowListAccessMixin

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
        has_pending_request = FollowRequest.objects.filter(from_user=self.object, to_user=self.request.user).exists()
        
        context['is_following'] = is_following
        context['is_requested'] = is_requested
        context['has_pending_request'] = has_pending_request
        context['saved_posts'] = SavedPost.objects.saved_posts(self.object)
        context['title'] = f'Comma | پروفایل {self.object.username}'
        context['active'] = 'profile'
        return context

class ProfileEditView(UserSpecificActionMixin, UpdateView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    form_class = CustomUserChangeForm
    
    def get_success_url(self):
        return reverse('account:profile', kwargs={'username': self.object.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | ویرایش پروفایل'
        context['active'] = 'profile'
        return context

class ActivityView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'account/activity.html'
    context_object_name = 'activities'

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Activity.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return response

class GetNewActivitiesCountView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            count = Activity.objects.filter(user=request.user, is_read=False).count()
            display_count = '99+' if count > 99 else str(count)
            return JsonResponse({'count': display_count})
        return JsonResponse({'count': '0'})

class FollowView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow == request.user:
            return JsonResponse({'status': 'error', 'message': 'شما نمیتوانید خودتان را فالو کنید.'})

        if user_to_follow.is_private:
            follow_request, created = FollowRequest.objects.get_or_create(from_user=request.user, to_user=user_to_follow)
            if created:
                Activity.create_activity(user=user_to_follow, activity_type='follow_request', actor=request.user)
                return JsonResponse({'status': 'success', 'action': 'request_sent'})
            else:
                return JsonResponse({'status': 'error', 'message': 'درخواست فالو قبلاً ارسال شده است.'})
        else:
            connection, created = UserConnection.objects.get_or_create(follower=request.user, following=user_to_follow)
            if created:
                Activity.create_activity(user=user_to_follow, activity_type='follow', actor=request.user)
                return JsonResponse({'status': 'success', 'action': 'followed'})
            else:
                return JsonResponse({'status': 'error', 'message': 'شما قبلاً این کاربر را فالو کرده‌اید.'})

class UnfollowView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_unfollow = get_object_or_404(User, username=username)
        UserConnection.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        return JsonResponse({'status': 'success', 'action': 'unfollowed'})

class AcceptFollowRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_accept = get_object_or_404(User, username=username)
        follow_request = FollowRequest.objects.filter(from_user=user_to_accept, to_user=request.user).first()

        if follow_request:
            UserConnection.objects.create(follower=user_to_accept, following=request.user)
            follow_request.delete()
            return JsonResponse({'status': 'success', 'action': 'request_accepted'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No follow request found.'})

class RejectFollowRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_to_reject = get_object_or_404(User, username=username)
        follow_request = FollowRequest.objects.get(from_user=request.user, to_user=user_to_reject)
        follow_request.delete()
        return JsonResponse({'status': 'success', 'action': 'request_cancelled'})
    
class PasswordResetView(AnonymousRequiredMixin, views.PasswordResetView):
    template_name = 'account/password_reset.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/email/password_reset_email.html'
    html_email_template_name = 'account/email/password_reset_email.html'
    subject_template_name = 'account/email/password_reset_subject.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | تغییر رمز عبور'
        return context

class PasswordResetDoneView(AnonymousRequiredMixin, views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | بازیابی رمز عبور'
        return context

class PasswordResetConfirmView(AnonymousRequiredMixin, views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | تغییر رمز عبور'
        return context

class PasswordResetCompleteView(AnonymousRequiredMixin, views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class FollowersView(LoginRequiredMixin, FollowListAccessMixin, ListView):
    template_name = 'account/follower_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return UserConnection.objects.filter(follower=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'follower'
        context['title'] = f'Comma | فالووینگ'
        return context

class FollowingView(LoginRequiredMixin, FollowListAccessMixin, ListView):
    template_name = 'account/follower_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return UserConnection.objects.filter(following=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Comma | فالوور'
        context['active'] = 'following'
        return context