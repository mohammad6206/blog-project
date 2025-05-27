from django.contrib.auth.views import PasswordResetView,PasswordResetCompleteView
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm,EmailOrUsernameAuthenticationForm  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:index')

    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('blog:index')
        else:
            context = {'form': form, 'login_active': True}
            return render(request, 'accounts/login.html', context)
    else:
        form = EmailOrUsernameAuthenticationForm(request=request)
        context = {'form': form, 'login_active': True}
        return render(request, 'accounts/login.html', context)



@login_required
def logout_view(request):
    logout(request)
    return redirect('blog:index')



def regester_view(request):
    if request.user.is_authenticated:
        return redirect('blog:index')  

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/regester.html', context)





class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'request': self.request,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'html_email_template_name': None,
            'extra_email_context': None,
        }
        form.save(**opts)
        return redirect(self.success_url)




class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
