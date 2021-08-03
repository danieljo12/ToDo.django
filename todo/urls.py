from django.urls import path
from .views import PostListView, PostUpdateView, PostDeleteView, UserPostListView, addTodo
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='todo-home'),
    path('user/', UserPostListView.as_view(), name='user-todos'),
    path('addTodo/', addTodo, name='todo-create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
]