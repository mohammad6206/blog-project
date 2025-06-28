from django import forms
from blog.models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder':'نام کاربری'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ایمیل'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'موضوع'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'متن'}),
        }
