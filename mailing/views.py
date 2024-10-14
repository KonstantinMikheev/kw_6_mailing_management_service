from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, TemplateView

from blog.models import Blog
from blog.services import get_posts_from_cache
from mailing.forms import ClientForm, EmailSettingForm, EmailSettingManagerForm
from mailing.models import Client, EmailSetting, MailingLog
from mailing.services import get_mailings_from_cache, get_clients_from_cache


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        mailings = get_mailings_from_cache()
        context_data['count_mailing'] = mailings.count()
        active_mailings_count = mailings.filter(is_active=True).count()
        context_data['active_mailings_count'] = active_mailings_count
        clients_from_cache = get_clients_from_cache()
        unique_clients_count = clients_from_cache.filter(is_active=True).distinct().count()
        context_data['unique_clients_count'] = unique_clients_count
        posts_from_cache = get_posts_from_cache()
        posts = list(posts_from_cache.filter(is_published=True))
        context_data['random_blog_posts'] = sample(posts, min(3, len(posts)))
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.owner = self.request.user
            new_client.save()
            return super().form_valid(form)
        else:
            raise PermissionDenied('Вы не можете создать клиента от другого пользователя.')


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def test_func(self):
        user = self.request.user
        return user == self.get_object().owner or self.request.user.is_superuser or self.request.user.groups.filter(
            name='manager').exists()


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = get_clients_from_cache()
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')



class EmailSettingListView(LoginRequiredMixin, ListView):
    model = EmailSetting

    def get_queryset(self):
        queryset = get_mailings_from_cache()
        return queryset


class EmailSettingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = EmailSetting

    def test_func(self):
        user = self.request.user
        return user == self.get_object().owner or self.request.user.is_superuser or self.request.user.groups.filter(
            name='manager').exists()



class EmailSettingCreateView(LoginRequiredMixin, CreateView):
    model = EmailSetting
    form_class = EmailSettingForm
    success_url = reverse_lazy('mailing:emailsetting_list')


    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            mailing = form.save()
            mailing.owner = user
            return super().form_valid(form)
        else:
            raise PermissionDenied('Вы не можете создать рассылку от другого пользователя.')

    def get_form_kwargs(self):
        """
        Передает объект запроса в класс формы. Это необходимо для отображения только тех членов,
        которые принадлежат данному пользователю
        """

        kwargs = super(EmailSettingCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class EmailSettingUpdateView(LoginRequiredMixin, UpdateView):
    model = EmailSetting
    form_class = EmailSettingForm
    success_url = reverse_lazy('mailing:emailsetting_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return EmailSettingForm
        if user.groups.filter(name='manager').exists():
            return EmailSettingManagerForm
        raise PermissionDenied

    def get_form_kwargs(self):
        """
        Передает объект запроса в класс формы. Это необходимо для отображения только тех членов,
        которые принадлежат данному пользователю
        """

        kwargs = super(EmailSettingUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class EmailSettingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailSetting
    success_url = reverse_lazy('mailing:emailsetting_list')

    def test_func(self):
        user = self.request.user
        return user == self.get_object().owner or self.request.user.is_superuser or self.request.user.groups.filter(
            name='manager').exists()


class MailingLogView(ListView):
    model = MailingLog
