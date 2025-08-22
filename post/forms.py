from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'id': 'subject', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'id': 'message', 'rows': 6, 'required': True}),
        }
        labels = {
            'subject': 'Subject *',
            'message': 'Message *',
        }
