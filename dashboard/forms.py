from django import forms
from blog.models import *



class PostForm(forms.ModelForm):

    author = forms.CharField(label='نویسنده',disabled=True, required=False)

    class Meta:
        model = Post
        fields = ['image', 'title', 'content', 'category', 'status']
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'image': 'تصویر',
            'title': 'عنوان',
            'content': 'متن',
            'category': 'دسته بندی',
            'status': 'وضعیت',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)   
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.author:
            self.fields['author'].initial = self.instance.author.username
        elif user:
            self.fields['author'].initial = user.username
        


class PackageForm(forms.ModelForm):
    class Meta:
        model = pakages
        fields = ['image', 'name', 'description', 'status', 'hotel', 'hotel_stars', 'max_count', 'price', 'Number_of_nights', 'location']
        labels = {

            'image': 'تصویر',
            'name': 'نام',
            'description': 'توضیحات',
            'status': 'وضعیت',
            'hotel': 'هتل',
            'hotel_stars': 'ستاره هتل',
            'max_count': 'تعداد نفرات',
            'price': 'قیمت',
            'Number_of_nights':'تعداد روز های اقامت در هتل',
            'location': 'مکان'
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            
            'name': 'نام'
        }


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_staff']

        labels = {
            
            'username': 'نام کاربری',
            'email': 'ایمیل',
            'password': 'رمز عبور',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'is_staff': 'مدیریت'
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)
        else:
            if user.pk:
                existing_user = CustomUser.objects.get(pk=user.pk)
                user.password = existing_user.password

        user.is_superuser = user.is_staff

        if commit:
            user.save()
        return user







class ContactReplyForm(forms.ModelForm):
    class Meta:
        model = ContactReply
        fields = ['reply_text']
        widgets = {
            'reply_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'پاسخ خود را اینجا بنویسید...'
            }),
        }
        labels = {
            'reply_text': 'متن پاسخ',
        }
