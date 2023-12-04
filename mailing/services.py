from datetime import datetime

from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config import settings
from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Logs


def send_order_email(obj: Mailing):
    try:
        send_mail(
            subject=obj.title_message,
            message=obj.body_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[*obj.client.all()],
            fail_silently=True)

        logs = Logs.objects.create(  # запись в таблицу Logs об успешности выполнения
            mailing=obj,
            datetime_of_last_attempt=datetime.now(),
            status=True,
            error_msg='200 OK'

        )
    except Exception as e:

        logs = Logs.objects.create(  # запись в таблицу Logs об ошибке
            mailing=obj,
            datetime_of_last_attempt=datetime.now(),
            status=False,
            error_msg=str(e)

        )


def time_task():
    # получение текущей даты
    current_date = datetime.now().date()

    # выборка из базы данных всех рассылок со статусом создана
    mailings_created = Mailing.objects.filter(status='created')

    # проверка пустой ли список или нет
    if mailings_created.exists():

        for mailing in mailings_created:
            # проверка пришло ли время рассылки
            if mailing.start_time <= current_date <= mailing.end_time:

                mailing.status = 'started'
                mailing.save()

    # выборка из базы данных всех рассылок со статусом запущено
    mailings_launched = Mailing.objects.filter(status='started')

    # проверка пустой ли список или нет
    if mailings_launched.exists():

        for mailing in mailings_launched:

            # проверка находится ли текущая дата внутри промежутка времени между началом и концом рассылки
            if mailing.start_time <= current_date <= mailing.end_time:

                # если до текущего момента уже был запуск рассылки
                if mailing.last_run:

                    # разница между текущей датой и последним запуском
                    differance = current_date - mailing.last_run

                    if mailing.period == 'daily':

                        # если разница между текущей датой и последней датой запуска равна 1 дню
                        if differance.days == 1:

                            # запуск рассылки
                            send_order_email(mailing)

                            # установление новой даты последнего запуска
                            mailing.last_run = current_date

                            mailing.save()

                    elif mailing.period == 'weekly':

                        # если разница между текущей датой и последней датой запуска равна 7 дням
                        if differance.days == 7:

                            # запуск рассылки
                            send_order_email(mailing)

                            # установление новой даты последнего запуска
                            mailing.last_run = current_date

                            mailing.save()

                    elif mailing.period == 'monthly':

                        # если разница между текущей датой и последней датой запуска равна 30 дням
                        if differance.days == 30:

                            # запуск рассылки
                            send_order_email(mailing)

                            # установление новой даты последнего запуска
                            mailing.last_run = current_date

                            mailing.save()

                # если рассылка ещё не запускалась
                else:

                    # запуск рассылки
                    send_order_email(mailing)  # запуск рассылки

                    # установление новой даты последнего запуска
                    mailing.last_run = current_date
                    mailing.save()

            # если текущая дата больше чем конец рассылки
            elif current_date >= mailing.end_time:

                mailing.status = 'done'

                mailing.save()


def cache_blog():
    if CACHE_ENABLED:
        # Проверяем включенность кеша
        key = f'blog_list'  # Создаем ключ для хранения
        blog_list = cache.get(key)  # Пытаемся получить данные
        if blog_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            blog_list = Blog.objects.all()
            cache.set(key, blog_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        blog_list = Blog.objects.all()
    # Возвращаем результат
    return blog_list
