from django.urls import path
from blog import views


app_name='blog'

urlpatterns = [
    path('',views.index_View,name='index'),
    path('about',views.about_View,name='about'),
    path('contact',views.contact_view,name='contact'),
    path('blog',views.blog_view,name='blog'),
    path('post_detail/<int:id>', views.post_detail_View, name='post_detail'),
    path('packages', views.packages_View, name='packages'),
    path('package/<int:id>/', views.package_detail, name='package_detail'),
    path('services', views.services_View, name='services'),
]
