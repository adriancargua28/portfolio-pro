from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Conversation, Message, DEFAULT_MODEL


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_create_conversation(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        self.assertEqual(str(conv), "testuser - Test")
        self.assertFalse(conv.is_archived)
        self.assertFalse(conv.is_pinned)

    def test_create_message(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        msg = Message.objects.create(conversation=conv, role=Message.ROLE_USER, content="Hello")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.feedback, "")

    def test_get_messages_for_api(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        Message.objects.create(conversation=conv, role="user", content="Hi")
        Message.objects.create(conversation=conv, role="assistant", content="Hello")
        messages = conv.get_messages_for_api()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_register(self):
        response = self.client.post(reverse("chat:register"), {
            "username": "newuser",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login(self):
        response = self.client.post(reverse("chat:login"), {
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        response = self.client.post(reverse("chat:login"), {
            "username": "testuser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)


class ConversationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")

    def test_conversation_list(self):
        response = self.client.get(reverse("chat:conversation_list"))
        self.assertEqual(response.status_code, 200)

    def test_conversation_new_get(self):
        response = self.client.get(reverse("chat:conversation_new"))
        self.assertEqual(response.status_code, 200)

    def test_conversation_new_post(self):
        response = self.client.post(reverse("chat:conversation_new"), {
            "title": "My Chat",
            "model": DEFAULT_MODEL,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Conversation.objects.filter(title="My Chat").exists())

    def test_conversation_detail(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        response = self.client.get(reverse("chat:conversation_detail", args=[conv.pk]))
        self.assertEqual(response.status_code, 200)

    def test_conversation_rename(self):
        conv = Conversation.objects.create(user=self.user, title="Old Title")
        response = self.client.post(reverse("chat:conversation_rename", args=[conv.pk]), {"title": "New Title"})
        conv.refresh_from_db()
        self.assertEqual(conv.title, "New Title")

    def test_conversation_pin(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        self.client.post(reverse("chat:conversation_pin", args=[conv.pk]))
        conv.refresh_from_db()
        self.assertTrue(conv.is_pinned)

    def test_conversation_archive(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        self.client.post(reverse("chat:conversation_archive", args=[conv.pk]))
        conv.refresh_from_db()
        self.assertTrue(conv.is_archived)

    def test_conversation_delete(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        self.client.post(reverse("chat:conversation_delete", args=[conv.pk]))
        self.assertFalse(Conversation.objects.filter(pk=conv.pk).exists())

    def test_message_feedback(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        msg = Message.objects.create(conversation=conv, role="assistant", content="Hi")
        self.client.post(reverse("chat:message_feedback", args=[msg.pk]), {"feedback": "like"})
        msg.refresh_from_db()
        self.assertEqual(msg.feedback, "like")

    def test_export_json(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        Message.objects.create(conversation=conv, role="user", content="Hello")
        response = self.client.get(reverse("chat:export_conversation", args=[conv.pk]) + "?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response["Content-Type"])

    def test_export_md(self):
        conv = Conversation.objects.create(user=self.user, title="Test")
        response = self.client.get(reverse("chat:export_conversation", args=[conv.pk]) + "?format=md")
        self.assertEqual(response.status_code, 200)

    def test_search_conversations(self):
        Conversation.objects.create(user=self.user, title="Python tips")
        Conversation.objects.create(user=self.user, title="Django help")
        response = self.client.get(reverse("chat:conversation_list") + "?q=Python")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python tips")

    def test_unauthenticated_redirect(self):
        self.client.logout()
        response = self.client.get(reverse("chat:conversation_list"))
        self.assertEqual(response.status_code, 302)


class FormTests(TestCase):
    def test_message_form_max_context(self):
        from .forms import MessageForm
        form = MessageForm(data={"content": "hi", "context_text": "x" * 2001})
        self.assertFalse(form.is_valid())

    def test_message_form_valid(self):
        from .forms import MessageForm
        form = MessageForm(data={"content": "Hello", "context_text": ""})
        self.assertTrue(form.is_valid())
