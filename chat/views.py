from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)

    if request.method == 'POST':
        caption = request.POST.get("message")
        if caption:
            Message.objects.create(chat=chat, sender=request.user, receiver=other_user, caption=caption)

        return redirect("chat", user_id=other_user.id)

    messages = chat.messages.order_by('timestamp')
    return render(request, "message/chat.html", {
        "chat": chat,
        "messages": messages,
        "other_user": other_user
    })
@login_required
def all_chats_view(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-date')
    return render(request, 'message/my_chats.html', {'chats': chats})