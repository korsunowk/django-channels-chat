from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from channels import Group
import json

from chat.forms import UserCreateForm
from chat.models import Chat, Message

# Create your views here.


class ChatPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data()

        if Chat.objects.count():
            context['messages'] = Chat.objects.first().messages.all()
        else:
            room = Chat.objects.create()
            room.recipients.add(self.request.user)

        return context


class UserCreateView(generic.CreateView):
    model = User
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message', None)
        sender = int(request.POST.get('sender', None))
        if message and sender:
            new_message = Message.objects.create(
                chat=Chat.objects.first(),
                sender=User.objects.get(pk=sender),
                text=message
            )

            recipient_message = render_to_string('partials/other-message-html.html', {'message': new_message})
            sender_message = render_to_string('partials/my-message-html.html', {'message': new_message})

            Group("room").send({
                "text": json.dumps({
                    "recipient_message": recipient_message,
                    "sender_message": sender_message,
                    "recipient": new_message.chat.recipients.all().exclude(pk=new_message.sender.pk).first().pk,
                    "sender": self.request.user.pk
                })
            })

            return JsonResponse(dict(recipient_message=recipient_message, sender_message=sender_message))
        return HttpResponse('')


class MessageTypingView(generic.View):
    def post(self, request, *args, **kwargs):
        user_pk = self.request.POST.get('user', 0)
        user = User.objects.get(pk=user_pk)
        Group("room").send({
            "text": json.dumps({
                'action': 'typing',
                'user': user_pk,
                'username': user.username
            }),
        })

        return HttpResponse("Hello, test")
