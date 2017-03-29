from django.contrib import admin
from chat.models import Chat, Message

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_sender_name', 'date']

    def get_sender_name(self, obj):
        return obj.sender.username

    get_sender_name.short_description = 'Sender username'


admin.site.register(Message, MessageAdmin)
