from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('activity/', views.ActivityView.as_view(), name='activity'),

    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit', views.ProfileEditView.as_view(), name='profile_edit'),

    path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<str:username>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),
    path('<str:username>/accept_request/', views.AcceptFollowRequestView.as_view(), name='accept_request'),
    path('<str:username>/reject_request/', views.RejectFollowRequestView.as_view(), name='reject_request'),
    
    path('get-new-activities-count/', views.GetNewActivitiesCountView.as_view(), name='get_new_activities_count'),
    
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]