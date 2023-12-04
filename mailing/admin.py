from django.contrib import admin

from mailing.models import Client, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment', 'owner',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'period', 'status',)
    list_filter = ('status',)
    search_fields = ('status',)
