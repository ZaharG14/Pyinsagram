from django.dispatch import receiver
from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )
    if request.method == 'POST':
       caption = request.POST.get("massage") or ""
       if caption.strip():
        Message.objects.create(sender=request.user, receiver=other_user, caption=caption)
       return redirect("chat", user_id=other_user.id)

    return render(request, "message/chat.html", {"messages": messages, "other_user": other_user})