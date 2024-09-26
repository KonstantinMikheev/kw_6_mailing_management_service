from django.contrib import admin

from mailing.models import Client, EmailSetting, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'email',)
    list_filter = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(EmailSetting)
class EmailSettingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)
    search_fields = ('subject', 'body',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_response', 'client', 'mailing',)
    list_filter = ('time', 'status', 'client', 'mailing')
    search_fields = ('time', 'status', 'server_response', 'client__email', 'mailing__subject')
