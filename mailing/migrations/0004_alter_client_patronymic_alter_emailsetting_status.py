# Generated by Django 5.1.1 on 2024-09-28 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_emailsetting_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество, если имеется'),
        ),
        migrations.AlterField(
            model_name='emailsetting',
            name='status',
            field=models.CharField(choices=[('create', 'Создана'), ('launched', 'Запущена'), ('completed', 'Завершена'), ('failed', 'Неудачная попытка')], default='create', max_length=50, verbose_name='Статус рассылки'),
        ),
    ]
