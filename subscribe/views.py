from django.urls import reverse

from django.shortcuts import render, get_object_or_404, redirect
from .models import Subscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def follow_toggle(request, username):
    subscribed_person = get_object_or_404(User, username=username)
    if subscribed_person == request.user:
        messages.error(request, "You cannot subscribe to yourself")
        return redirect(reverse('user:profile', kwargs={'username': username}))

    sub, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        subscribed_person=subscribed_person
    )
    if not created:
        sub.delete()
        messages.success(request, f"You have unsubscribed from {username}.")
    else:
        messages.success(request, f"You are now subscribed to {username}.")

    return redirect(reverse('details', kwargs={'id': subscribed_person.id}))