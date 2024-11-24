from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),

    path('create/', views.CreatePostView.as_view(), name='create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),

    path('post/<int:post_id>/save/', views.SavePostView.as_view(), name='save'),
    path('post/<int:post_id>/like/', views.LikePostView.as_view(), name='like'),
]