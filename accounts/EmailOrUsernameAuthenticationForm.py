from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class EmailOrUsernameAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(label="Email or Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            # بررسی اینکه ورودی ایمیل است یا یوزرنیم
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    raise forms.ValidationError("ایمیل یا نام کاربری وارد شده صحیح نیست.")
            else:
                username = username_or_email

            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("نام کاربری یا رمز عبور اشتباه است.")
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
