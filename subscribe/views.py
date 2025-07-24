from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()

@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect('profile', username=username)  # не можна підписатися на себе

    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        subscribed_person=target_user
    )
    if not created:
        subscription.delete()

    return redirect('profile', username=username)