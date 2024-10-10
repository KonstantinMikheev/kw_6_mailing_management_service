from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    IndexView, EmailSettingListView, EmailSettingDetailView, EmailSettingCreateView, EmailSettingUpdateView, \
    EmailSettingDeleteView, MailingLogView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('emailsetting', EmailSettingListView.as_view(), name='emailsetting_list'),
    path('emailsetting/<int:pk>/', cache_page(60)(EmailSettingDetailView.as_view()),
         name='emailsetting_detail'),
    path('emailsetting/create/', EmailSettingCreateView.as_view(), name='emailsetting_create'),
    path('emailsetting/<int:pk>/update/', EmailSettingUpdateView.as_view(), name='emailsetting_update'),
    path('emailsetting/<int:pk>/delete/', EmailSettingDeleteView.as_view(), name='emailsetting_delete'),
    path('mailinglog_list/', MailingLogView.as_view(), name='mailinglog_list'),
]
