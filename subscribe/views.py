from audioop import reverse

from django.shortcuts import render, get_object_or_404, redirect
from .models import Subscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def follow_toggle(request, username):
    subscribed_person = get_object_or_404(User, username)
    if subscribed_person == request.user:
        messages.error(request, "You cannot subscribe to yourself")
        return redirect(reverse('user:profile', kwargs={'username': username}))

    sub, created = Subscription.objects.get_or_create(
        subscrer=request.user,
        subscribed_person=subscribed_person
    )
    if not created:
        sub.delete()
        messages.success(request, f"You have unsubscribed from {username}.")
    else:
        messages.success(request, f"You are now subscribed to {username}.")

    return redirect(reverse('user:profile', kwargs={'username': username}))

@login_required
def follow_toggle_view(request, pk):
    target = get_object_or_404(User, pk=pk)
    profile = target.profile  # або інша логіка

    if profile.followers.filter(pk=request.user.pk).exists():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)

    return redirect('profile', pk=pk)