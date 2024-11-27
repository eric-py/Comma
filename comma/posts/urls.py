from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),

    path('create/', views.CreatePostView.as_view(), name='create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),
    
    path('search/', views.SearchView.as_view(), name='search'),

    path('post/<int:post_id>/save/', views.SavePostView.as_view(), name='save'),
    path('post/<int:post_id>/like/', views.LikePostView.as_view(), name='like'),
    
    path('post/<int:post_id>/add_comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('post/<int:post_id>/add_reply/', views.AddReplyView.as_view(), name='add_reply'),
    path('comment/<int:comment_id>/like/', views.LikeCommentView.as_view(), name='like_comment'),
]