from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm, BlogModeratorForm
from blog.models import Blog
from blog.services import get_posts_from_cache


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            blog = form.save()
            blog.author = user
            return super().form_valid(form)
        else:
            raise PermissionDenied('Вы не можете создать статью c другим автором.')


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """Метод для выбора формы в зависимости от прав доступа пользователя"""
        user = self.request.user  # Получаем текущего пользователя
        if user == self.object.author:
            return BlogForm
        elif user.groups.filter(name='content_manager').exists() or user.is_superuser:
            return BlogModeratorForm
        else:
            raise PermissionDenied


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        # queryset = super().get_queryset(*args, **kwargs)
        queryset = get_posts_from_cache()
        queryset = queryset.filter(is_published=True)  # Скрывает деактивированные статьи
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        user = self.request.user
        return user == self.get_object().author or self.request.user.is_superuser or self.request.user.groups.filter(
            name='content_manager').exists()


@login_required
@permission_required
def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()
    return redirect(reverse('blog:list'))
