from django.db import models
from django.contrib.auth.models import User


AVAILABLE_MODELS = [
    ("meta/llama-3.1-8b-instruct", "Llama 3.1 8B"),
    ("meta/llama-3.1-70b-instruct", "Llama 3.1 70B"),
    ("microsoft/phi-3-mini-128k-instruct", "Phi-3 Mini"),
    ("google/gemma-2-9b-it", "Gemma 2 9B"),
    ("mistralai/mistral-7b-instruct-v0.3", "Mistral 7B"),
]

DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    title = models.CharField(max_length=200, default="Nueva conversación")
    model = models.CharField(max_length=100, default=DEFAULT_MODEL)
    is_archived = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-updated_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def get_messages_for_api(self):
        messages = []
        for msg in self.messages.order_by("created_at"):
            messages.append({"role": msg.role, "content": msg.content})
        return messages


class Message(models.Model):
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ASSISTANT, "Assistant"),
    ]
    FEEDBACK_CHOICES = [
        ("like", "👍 Útil"),
        ("dislike", "👎 No útil"),
        ("", "Sin valorar"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    feedback = models.CharField(max_length=10, choices=FEEDBACK_CHOICES, blank=True, default="")
    tokens_used = models.IntegerField(default=0)
    response_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"
