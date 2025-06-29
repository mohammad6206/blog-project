
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from blog.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")



from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django import forms

CustomUser = get_user_model()

class EmailOrUsernameAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(label="ایمیل یا نام کاربری")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        user_obj = None

        if username_or_email and password:
            # ۱. پیدا کردن یوزر (بدون احراز هویت)
            if '@' in username_or_email:
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                except CustomUser.DoesNotExist:
                    raise forms.ValidationError("ایمیل  وارد شده وجود ندارد")
            else:
                try:
                    user_obj = CustomUser.objects.get(username=username_or_email)
                except CustomUser.DoesNotExist:
                    raise forms.ValidationError("نام کاربری وارد شده وجود ندارد")

            # ۲. بررسی فعال بودن
            if not user_obj.is_active:
                raise forms.ValidationError("حساب شما توسط ادمین غیرفعال شده است")

            # ۳. احراز هویت
            user = authenticate(self.request, username=user_obj.username, password=password)
            if user is None:
                raise forms.ValidationError("نام کاربری یا رمز عبور اشتباه است.")

            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
