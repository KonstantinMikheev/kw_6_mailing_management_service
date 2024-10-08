import datetime
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import EmailSetting, MailingLog


def send_email(email_setting):
    """Отправка рассылки на указанные адреса"""
    try:
        send_mail(
            subject=email_setting.subject,
            message=email_setting.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in email_setting.client.all() if client.is_active==True],
            fail_silently=False,
        )
        print('Отправлено')

        MailingLog.objects.create(
            time=datetime.datetime.now(datetime.timezone.utc),
            status=True,
            server_response="Сообщение отправлено получателям",
            mailing=email_setting,
            client=email_setting.client.first()  # для лога используется первый клиент из списка
        )
        print("Лог создан")

    except smtplib.SMTPException as e:
        # Если почта не отправлена, создаем лог с соответствующим статусом и сообщением об ошибке
        MailingLog.objects.create(
            time=datetime.datetime.now(datetime.timezone.utc),
            status=False,
            server_response=str(e),
            mailing=email_setting,
            client=email_setting.client.first()  # для лога используется первый клиент из списка
        )
        print(f'Ошибка при отправке рассылки: {str(e)}, лог создан')


def send_mailing():
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    # создание объекта с применением фильтра
    mailings = EmailSetting.objects.filter(start_from__lte=current_datetime).filter(is_active=True).filter(
        status__in=["Создана", "Запущена"])

    for mailing in mailings:
        # Проверяем, находится ли текущее время в диапазоне дат начала и конца рассылки
        if mailing.start_from <= current_datetime <= mailing.stop_at:

            mailing_log = MailingLog.objects.filter(mailing__id=mailing.pk)

            if mailing_log.exists():
                time_of_last_try = mailing_log.order_by('-time').first().time
                if mailing.periodicity == EmailSetting.DAILY:
                    if (current_datetime - time_of_last_try).days >= 1:
                        send_email(mailing)
                elif mailing.periodicity == EmailSetting.WEEKLY:
                    if (current_datetime - time_of_last_try).days >= 7:
                        send_email(mailing)
                elif mailing.periodicity == EmailSetting.MONTHLY:
                    if (current_datetime - time_of_last_try).days >= 30:
                        send_email(mailing)
                elif mailing.periodicity == EmailSetting.YEARLY:
                    if (current_datetime - time_of_last_try).days >= 365:
                        send_email(mailing)
            else:
                send_email(mailing)
                mailing.status = EmailSetting.LAUNCHED
                mailing.save()


        elif mailing.stop_at < current_datetime:
            # Если текущее время вышло за диапазон конца рассылки, останавливаем рассылку
            mailing.status = EmailSetting.COMPLETED
            mailing.save()
