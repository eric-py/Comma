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

    path('<str:username>/follow/', views.FollowToggleView.as_view(), name='follow'),
    
    path('get-new-activities-count/', views.GetNewActivitiesCountView.as_view(), name='get_new_activities_count'),
]