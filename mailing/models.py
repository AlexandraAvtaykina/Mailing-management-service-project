from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=300, verbose_name='комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'


class Mailing(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Ежедневная'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('done', 'Завершена')

    ]

    start_time = models.DateField(**NULLABLE, verbose_name='начало рассылки')
    end_time = models.DateField(**NULLABLE, verbose_name='конец рассылки')
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, **NULLABLE, verbose_name='периодичность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='статус рассылки')
    client = models.ManyToManyField(Client, verbose_name='клиент')
    title_message = models.CharField(max_length=100, verbose_name='тема письма')
    body_message = models.TextField(verbose_name='тело письма', **NULLABLE)

    last_run = models.DateField(verbose_name='дата последней отправки рассылки', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} ({self.status} {self.client})'

    class Meta:
        verbose_name = 'Рассылка (настройки)'
        verbose_name_plural = 'Рассылки (настройки)'

    permissions = [
        (
            'deactivate_mailing',
            'Can deactivate settings'
        )
    ]


class Logs(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )
    datetime_of_last_attempt = models.DateTimeField(verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус попытки')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name='рассылка')
    error_msg = models.TextField(**NULLABLE, verbose_name='error msg')

    def __str__(self):
        return f'{self.datetime_of_last_attempt} {self.status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
