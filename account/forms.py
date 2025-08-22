from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import VerificationCode, CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2', 'image_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['image_profile'].widget.attrs.update({'class': 'form-control', 'required': False})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email has already been registered')
        return email



class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label='Verification Code', widget=forms.TextInput(attrs={
        'class': 'form-control text-center',
        'placeholder': '000000'
    }))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError('Code must be a 6-digit number.')
        return code

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'image_profile']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'id':'profileFirstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'id':'profileLastName'}),
            'bio': forms.Textarea(attrs={'class':'form-control','rows':4, 'id':'profileBio'},),
            'image_profile': forms.FileInput(attrs={'class':'form-control', 'id':'profileImageUpload'}),
        }
