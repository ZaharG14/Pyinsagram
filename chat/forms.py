from django import forms
from .models import Contact, Message

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['caption']