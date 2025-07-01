from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from .models import Contact


@login_required
def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect ('contact_list')
    else:
        form = ContactForm()

        return render(request, 'contacts/add_contact.html', {'form': form})

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(owner=request.user)
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})