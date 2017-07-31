from django.conf.urls import url
from chat import views

app_name = 'chat'
urlpatterns = [
    url(r'^$', views.ChatPageView.as_view(), name='chat_page'),
    url(r'^create/$', views.MessageCreateView.as_view(), name='create'),
    url(r'^typing/$', views.MessageTypingView.as_view(), name='typing'),
    url('^registration/', views.UserCreateView.as_view(), name='registration')
]
