from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество, если имеется', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email', unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    owner = models.ForeignKey(User, verbose_name='владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.last_name} {self.first_name} {self.patronymic if self.patronymic else ""})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class EmailSetting(models.Model):
    ONCE = 'Однократно'
    DAILY = 'Ежедневно'
    WEEKLY = 'Еженедельно'
    MONTHLY = 'Ежемесячно'
    YEARLY = 'Ежегодно'
    PERIODICITY_CHOICES = [
        (ONCE, 'Однократно'),
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
        (YEARLY, 'ежегодно'),
    ]
    CREATED = 'Создана'
    LAUNCHED = 'Запущена'
    COMPLETED = 'Завершена'
    STATUS_MAILING = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    subject = models.CharField(max_length=250, verbose_name='Тема рассылки')
    body = models.TextField(verbose_name='Текст рассылки')
    description = models.TextField(verbose_name='Описание рассылки', **NULLABLE)
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    start_from = models.DateTimeField(verbose_name='Дата начала отправки')
    stop_at = models.DateTimeField(verbose_name='Дата окончания отправки')
    status = models.CharField(max_length=50, choices=STATUS_MAILING, verbose_name='Статус рассылки', default='Создана')
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    owner = models.ForeignKey(User, verbose_name='владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.subject} time: {self.start_from} - {self.stop_at}, periodicity: {self.periodicity}, status: {self.status}'

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылок'


class MailingLog(models.Model):
    time = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.BooleanField(verbose_name='статус попытки', default=False, )
    server_response = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailing = models.ForeignKey(EmailSetting, on_delete=models.PROTECT, verbose_name='рассылка', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='клиент рассылки', **NULLABLE)


def __str__(self):
    return f'{self.last_attempt_time} {self.status}'


class Meta:
    verbose_name = 'Попытка рассылки'
    verbose_name_plural = 'Попытки рассылок'
