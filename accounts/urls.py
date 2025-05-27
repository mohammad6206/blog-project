from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views
from django.urls import reverse_lazy


app_name = 'accounts'  

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('regester/', views.regester_view, name='regester'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',success_url=reverse_lazy('accounts:password_reset_complete')),name='password_reset_confirm'),    
    path('reset/done/',views.CustomPasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
