from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, TemplateView

from mailing.forms import ClientForm, EmailSettingForm
from mailing.models import Client, EmailSetting, MailingLog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        context_data['count_mailing'] = EmailSetting.objects.all().count()
        active_mailings_count = EmailSetting.objects.filter(is_active=True).count()
        context_data['active_mailings_count'] = active_mailings_count
        unique_clients_count = Client.objects.filter(is_active=True).distinct().count()
        context_data['unique_clients_count'] = unique_clients_count
        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = 'mailing:client_list'



class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = 'mailing:client_list'


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class EmailSettingListView(ListView):
    model = EmailSetting


class EmailSettingDetailView(DetailView):
    model = EmailSetting


class EmailSettingCreateView(CreateView):
    model = EmailSetting
    form_class = EmailSettingForm
    success_url = reverse_lazy('mailing:emailsetting_list')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class EmailSettingUpdateView(UpdateView):
    model = EmailSetting
    form_class = EmailSettingForm
    success_url = reverse_lazy('mailing:emailsetting_list')

    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.owner:
    #         return EmailSettingForm
    #     if user.has_perm('mailing.view_all_mailings') and user.has_perm('mailings.deactivate_mailing'):
    #         return ModeratorEmailSettingForm
    #     raise PermissionDenied


class EmailSettingDeleteView(DeleteView):
    model = EmailSetting
    success_url = reverse_lazy('mailing:emailsetting_list')


class MailingLogView(ListView):
    model = MailingLog

