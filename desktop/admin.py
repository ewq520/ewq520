from django.contrib import admin

# Register your models here.
from .utilities import send_activation_notification
from .models import AdvUser
admin.site.register(AdvUser)

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с оповещениями отправлены')
send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации'