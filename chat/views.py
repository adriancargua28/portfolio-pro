import json
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from .models import Conversation, Message, AVAILABLE_MODELS
from .forms import RegisterForm, LoginForm, ConversationForm, MessageForm, SearchForm
from .llm import get_llm_response


def index(request):
    if request.user.is_authenticated:
        return redirect("chat:conversation_list")
    return render(request, "chat/index.html")


def about(request):
    return render(request, "chat/about.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("chat:conversation_list")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Cuenta creada con éxito!")
            return redirect("chat:conversation_list")
    else:
        form = RegisterForm()
    return render(request, "chat/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("chat:conversation_list")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect(request.GET.get("next", "chat:conversation_list"))
    else:
        form = LoginForm(request)
    return render(request, "chat/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("chat:index")


@login_required
def conversation_list(request):
    search_form = SearchForm(request.GET)
    q = request.GET.get("q", "").strip()

    conversations = Conversation.objects.filter(user=request.user, is_archived=False)

    if q:
        conversations = conversations.filter(
            Q(title__icontains=q) | Q(messages__content__icontains=q)
        ).distinct()

    pinned = conversations.filter(is_pinned=True)
    unpinned = conversations.filter(is_pinned=False)

    archived = Conversation.objects.filter(user=request.user, is_archived=True)

    return render(request, "chat/conversation_list.html", {
        "pinned": pinned,
        "unpinned": unpinned,
        "archived": archived,
        "search_form": search_form,
        "q": q,
        "available_models": AVAILABLE_MODELS,
    })


@login_required
def conversation_new(request):
    if request.method == "POST":
        form = ConversationForm(request.POST)
        if form.is_valid():
            conv = form.save(commit=False)
            conv.user = request.user
            conv.save()
            return redirect("chat:conversation_detail", pk=conv.pk)
    else:
        form = ConversationForm()
    return render(request, "chat/conversation_new.html", {"form": form})


@login_required
def conversation_detail(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    form = MessageForm()
    return render(request, "chat/conversation_detail.html", {
        "conversation": conv,
        "messages_list": conv.messages.all(),
        "form": form,
        "available_models": AVAILABLE_MODELS,
    })


@login_required
@require_POST
def send_message(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    form = MessageForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Error en el formulario", status=400)

    content = form.cleaned_data["content"].strip()
    context_text = form.cleaned_data.get("context_text", "").strip()

    if not content:
        return HttpResponse("Mensaje vacío", status=400)

    # Build user message content with optional context
    user_content = content
    if context_text:
        user_content = f"[Contexto adicional]\n{context_text}\n\n[Pregunta]\n{content}"

    # Save user message
    Message.objects.create(conversation=conv, role=Message.ROLE_USER, content=content)

    # Build messages for API
    api_messages = conv.get_messages_for_api()
    if context_text:
        # Replace last user message with enriched version
        api_messages[-1]["content"] = user_content

    # Call LLM
    result = get_llm_response(api_messages, model=conv.model)

    # Save assistant message
    assistant_msg = Message.objects.create(
        conversation=conv,
        role=Message.ROLE_ASSISTANT,
        content=result["content"],
        tokens_used=result.get("tokens", 0),
        response_time_ms=result.get("response_time_ms", 0),
    )

    # Update conversation timestamp
    conv.save()

    return redirect("chat:conversation_detail", pk=pk)


@login_required
@require_POST
def conversation_rename(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    new_title = request.POST.get("title", "").strip()
    if new_title:
        conv.title = new_title[:200]
        conv.save()
    return redirect("chat:conversation_detail", pk=pk)


@login_required
@require_POST
def conversation_archive(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    conv.is_archived = not conv.is_archived
    conv.save()
    return redirect("chat:conversation_list")


@login_required
@require_POST
def conversation_pin(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    conv.is_pinned = not conv.is_pinned
    conv.save()
    return redirect("chat:conversation_list")


@login_required
@require_POST
def conversation_delete(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    conv.delete()
    return redirect("chat:conversation_list")


@login_required
@require_POST
def conversation_change_model(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    model = request.POST.get("model", "")
    valid_models = [m[0] for m in AVAILABLE_MODELS]
    if model in valid_models:
        conv.model = model
        conv.save()
    return redirect("chat:conversation_detail", pk=pk)


@login_required
@require_POST
def message_feedback(request, msg_pk):
    msg = get_object_or_404(Message, pk=msg_pk, conversation__user=request.user)
    feedback = request.POST.get("feedback", "")
    if feedback in ("like", "dislike", ""):
        msg.feedback = feedback
        msg.save()
    return redirect("chat:conversation_detail", pk=msg.conversation.pk)


@login_required
def export_conversation(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, user=request.user)
    fmt = request.GET.get("format", "json")

    if fmt == "md":
        lines = [f"# {conv.title}\n", f"*Modelo: {conv.model}*\n", f"*Fecha: {conv.created_at.strftime('%Y-%m-%d %H:%M')}*\n\n---\n"]
        for msg in conv.messages.all():
            prefix = "**Tú**" if msg.role == "user" else "**Asistente**"
            lines.append(f"{prefix}:\n{msg.content}\n\n")
        content = "".join(lines)
        response = HttpResponse(content, content_type="text/markdown")
        response["Content-Disposition"] = f'attachment; filename="conversation_{pk}.md"'
        return response

    else:  # json
        data = {
            "id": conv.pk,
            "title": conv.title,
            "model": conv.model,
            "created_at": conv.created_at.isoformat(),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                    "feedback": msg.feedback,
                }
                for msg in conv.messages.all()
            ],
        }
        response = HttpResponse(json.dumps(data, ensure_ascii=False, indent=2), content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="conversation_{pk}.json"'
        return response


@login_required
def metrics_view(request):
    """Basic metrics view accessible to staff."""
    if not request.user.is_staff:
        return redirect("chat:conversation_list")

    from django.contrib.auth.models import User
    total_conversations = Conversation.objects.count()
    total_messages = Message.objects.count()
    total_users = User.objects.count()
    likes = Message.objects.filter(feedback="like").count()
    dislikes = Message.objects.filter(feedback="dislike").count()

    model_usage = {}
    for model_id, model_name in AVAILABLE_MODELS:
        count = Conversation.objects.filter(model=model_id).count()
        model_usage[model_name] = count

    return render(request, "chat/metrics.html", {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "total_users": total_users,
        "likes": likes,
        "dislikes": dislikes,
        "model_usage": model_usage,
    })
