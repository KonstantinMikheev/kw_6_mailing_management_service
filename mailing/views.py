from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, TemplateView

from mailing.forms import ClientForm, EmailSettingForm
from mailing.models import Client, EmailSetting, MailingLog


class StartPageView(TemplateView):
    template_name = 'mailing/start_page.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', args=[self.kwargs.get('pk')])


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', args=[self.kwargs.get('pk')])


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
    success_url = reverse_lazy('mailings:mailingsettings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingSettingsForm
        if user.has_perm('mailings.view_all_mailings') and user.has_perm('mailings.deactivate_mailing'):
            return ModeratorMailingSettingsForm
        raise PermissionDenied


class EmailSettingDeleteView(DeleteView):
    model = EmailSetting
    success_url = reverse_lazy('mailings:mailingsettings_list')


class MailingLogView(ListView):
    model = MailingLog