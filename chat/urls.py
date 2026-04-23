from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("conversations/", views.conversation_list, name="conversation_list"),
    path("conversations/new/", views.conversation_new, name="conversation_new"),
    path("conversations/<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("conversations/<int:pk>/send/", views.send_message, name="send_message"),
    path("conversations/<int:pk>/stream/", views.stream_message, name="stream_message"),
    path("conversations/<int:pk>/rename/", views.conversation_rename, name="conversation_rename"),
    path("conversations/<int:pk>/archive/", views.conversation_archive, name="conversation_archive"),
    path("conversations/<int:pk>/pin/", views.conversation_pin, name="conversation_pin"),
    path("conversations/<int:pk>/delete/", views.conversation_delete, name="conversation_delete"),
    path("conversations/<int:pk>/change-model/", views.conversation_change_model, name="conversation_change_model"),
    path("conversations/<int:pk>/export/", views.export_conversation, name="export_conversation"),
    path("messages/<int:msg_pk>/feedback/", views.message_feedback, name="message_feedback"),
    path("metrics/", views.metrics_view, name="metrics"),
]
