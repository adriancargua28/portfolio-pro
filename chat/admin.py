from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "model", "is_pinned", "is_archived", "message_count", "updated_at"]
    list_filter = ["is_archived", "is_pinned", "model", "user"]
    search_fields = ["title", "user__username"]
    readonly_fields = ["created_at", "updated_at"]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Mensajes"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["conversation", "role", "short_content", "feedback", "tokens_used", "response_time_ms", "created_at"]
    list_filter = ["role", "feedback", "conversation__user"]
    search_fields = ["content", "conversation__title"]
    readonly_fields = ["created_at"]

    def short_content(self, obj):
        return obj.content[:80]
    short_content.short_description = "Contenido"
