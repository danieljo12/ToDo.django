from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView,UpdateView, DeleteView
from .models import TodoPost
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

class PostListView(ListView):
    model = TodoPost
    # set a new template so we can use the existing template we awnt
    template_name = 'todo/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = TodoPost
    # set a new template so we can use the existing template we awnt
    template_name = 'todo/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # makes sure that only the user
    def test_func(self):

        if self.request.user.is_authenticated:
            return True
        else:
            return False

    def get_queryset(self):
        user = get_object_or_404(User, username= self.request.user)        
        return TodoPost.objects.filter(author=user).order_by('-date_posted')

def addTodo(request):
    if request.method == 'POST':
        new_item = TodoPost(content = request.POST['content'], author=  request.user)
        new_item.save()
    
    return HttpResponseRedirect('/user/')

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = TodoPost
    fields = ['content']
    success_url = '/user/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = TodoPost
    success_url = '/user/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False