from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('packages/', views.package_list, name='package_list'),
    path('categories/', views.category_list, name='category_list'),
    path('users/', views.users_list, name='users_list'),
    path('messages/', views.messages_list, name='messages_list'),
    path('dashboard/contacts/<int:pk>/', views.contact_message_detail, name='contact_message_detail'),
    path('contacts/reply/<int:pk>/', views.contact_reply_create, name='contact_reply'),
    path('reply/delete/<int:pk>/', views.reply_delete, name='reply_delete'),
    path('contacts/delete/<int:pk>/', views.contact_delete, name='contact_delete'),
    path('posts/create/',views.create_post, name='posts_create'),
    path('posts/<int:pk>/update/', views.update_post, name='posts_update'),
    path('posts/<int:pk>/delete/', views.delete_post, name='posts_delete'),
    path('packages/create/', views.create_package, name='packages_create'),
    path('packages/<int:pk>/update/', views.update_package, name='packages_update'),
    path('packages/<int:pk>/delete/', views.delete_package, name='packages_delete'),
    path('categories/create/', views.create_category, name='categories_create'),
    path('categories/<int:pk>/update/', views.update_category, name='categories_update'),
    path('categories/<int:pk>/delete/', views.delete_category, name='categories_delete'),
    path('users/create/', views.create_user, name='users_create'),
    path('users/<int:pk>/update/', views.update_user, name='users_update'),
    path('users/<int:pk>/delete/', views.delete_user, name='users_delete'),
    path('users/<int:pk>/activate/', views.activate_user, name='users_activate'),
    path('users/<int:pk>/deactivate/', views.deactivate_user, name='users_deactivate'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),

]
handler403 = 'dashboard.views.permission_denied_view'