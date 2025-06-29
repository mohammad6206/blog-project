from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.shortcuts import render, redirect,get_object_or_404
from blog.models import *
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import logout,authenticate,login,get_user_model 
from django.contrib import messages
from dashboard.decorator import superuser_required
from dashboard.forms import *
import jdatetime
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.

User = get_user_model()

def get_online_user_ids():
    sessions = Session.objects.filter(expire_date__gte=now())
    user_ids = []
    for session in sessions:
        data = session.get_decoded()
        uid = data.get('_auth_user_id')
        if uid:
            user_ids.append(int(uid))
    return set(user_ids)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
            return render(request, '403.html', status=403)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                user.ip = get_client_ip(request)
                user.login_count += 1
                user.save()

                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, '403.html', status=403)
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.', extra_tags='login')

    return render(request, 'dashboard/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)



@superuser_required
def dashboard_home(request):
    posts = Post.objects.all()
    pakages_qs = pakages.objects.all()
    categories_qs = Category.objects.all()
    users_qs = CustomUser.objects.all()
    contact_messages = ContactMessage.objects.order_by('-created_date')[:5]  

    posts_count = posts.count()
    pakages_count = pakages_qs.count()
    categories_count = categories_qs.count()
    users_count = users_qs.count()

    monthly_data = (
        posts.filter(status=True)
        .annotate(month=TruncMonth('published_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    chart_labels = [
        jdatetime.date.fromgregorian(date=item['month']).strftime('%Y/%m/%d') 
        for item in monthly_data
    ]
    chart_data = [item['count'] for item in monthly_data]
        
    raw_status_counts = posts.values('status').annotate(total=Count('id'))

    status_counts = {
        'منتشر شده': next((item['total'] for item in raw_status_counts if item['status'] is True ), 0),
        'منتشر نشده': next((item['total'] for item in raw_status_counts if item['status'] is False), 0),
    }

    pakages_status_counts = {
        'فعال': pakages_qs.filter(status=True).count(),
        'غیرفعال': pakages_qs.filter(status=False).count()
    }

    user_activity_counts = {
        'فعال': users_qs.filter(login_count__gte=10).count(),     
        'نیمه فعال': users_qs.filter(login_count__gte=3, login_count__lt=10).count(),
        'غیرفعال': users_qs.filter(login_count__lt=3).count(),
    }

    category_post_counts = (
        categories_qs
        .annotate(post_count=Count('post'))
        .values_list('name', 'post_count')
    )
    category_labels = [item[0] for item in category_post_counts]
    category_post_counts_data = [item[1] for item in category_post_counts]

    top_posts = posts.order_by('-counted_view')[:5]

    users = User.objects.all()
    online_user_ids = get_online_user_ids()
    
    for user in users:
        user.is_online = user.id in online_user_ids

    sorted_users = sorted(users, key=lambda u: (not u.is_online, u.last_login or now()), reverse=False)

    return render(request, 'dashboard/dashboard.html', {
        'contact_messages': contact_messages,
        "users_recent": sorted_users,  
        'posts_count': posts_count,
        'pakages_count': pakages_count,
        'categories_count': categories_count,
        'users_count': users_count,
        'chart_labels': json.dumps(chart_labels, cls=DjangoJSONEncoder),
        'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder),
        'status_counts': json.dumps(status_counts, cls=DjangoJSONEncoder),
        'pakages_status_counts': json.dumps(pakages_status_counts, cls=DjangoJSONEncoder),
        'user_activity_counts': json.dumps(user_activity_counts, cls=DjangoJSONEncoder),
        'category_labels': json.dumps(category_labels, cls=DjangoJSONEncoder),
        'category_post_counts': json.dumps(category_post_counts_data, cls=DjangoJSONEncoder),
        'top_posts': top_posts,
    })






@superuser_required
def contact_reply_create(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)

    if hasattr(message, 'reply'):
        messages.warning(request, "برای این پیام قبلاً پاسخی ثبت شده است.")
        return redirect('contact_message_detail')  

    if request.method == 'POST':
        form = ContactReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.message = message
            reply.replied_by = request.user
            reply.save()
            messages.success(request, "پاسخ با موفقیت ثبت شد.")
            return redirect('contact_message_detail')
    else:
        form = ContactReplyForm()

    return render(request, 'dashboard/contact_reply_form.html', {'form': form, 'message': message})




@staff_member_required
def reply_delete(request, pk):
    reply = get_object_or_404(ContactReply, pk=pk)
    message_pk = reply.message.pk 
    if request.method == 'POST':
        reply.delete()
        messages.success(request, "پاسخ با موفقیت حذف شد.")
        return redirect('contact_message_detail', pk=message_pk)


@superuser_required
def contact_delete(request, pk):
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        contact_message.delete()
        messages.success(request, 'پیام حذف شد')
        return redirect('messages_list')
    return render(request, 'dashboard/confirm_delete_message.html', {
        'object': contact_message,
        'title': 'حذف پیام'
    })



@superuser_required
def messages_list(request):
    messages =ContactMessage.objects.all().order_by('id')
    return render(request, 'dashboard/messages_list.html', {
        'contact_messages': messages
    })


@superuser_required  
def contact_message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    replies = message.replies.all().order_by('-replied_at')
    form = ContactReplyForm()

    if request.method == 'POST':
        form = ContactReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.message = message
            reply.replied_by = request.user
            reply.save()

            context = {
                'name': message.name,
                'subject': message.subject or 'بدون موضوع',
                'reply_text': reply.reply_text,
            }

            html_content = render_to_string('dashboard/replay_notification.html', context)
            text_content = f"""سلام {message.name} عزیز

شما پیامی برای ما ارسال کرده بودید با موضوع: {context['subject']}

پاسخ مدیریت سایت:
{reply.reply_text}

با تشکر،
تیم پشتیبانی Travela
"""

            email = EmailMultiAlternatives(
                subject='پاسخ به پیام شما',
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[message.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "پاسخ با موفقیت ثبت و ایمیل ارسال شد.")
            return redirect('contact_message_detail', pk=pk)
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")

    return render(request, 'dashboard/contact_message_detail.html', {
        'message': message,
        'replies': replies,
        'form': form,
    })



@superuser_required
def post_list(request):
    posts = Post.objects.all().order_by('id')
    return render(request, 'dashboard/post_list.html', {'posts': posts})


@superuser_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=True)
    return render(request, 'dashboard/post_detail.html', {'post': post})

@superuser_required
def package_list(request):
    packages = pakages.objects.all().order_by('id')
    return render(request, 'dashboard/package_list.html', {'packages': packages})


@superuser_required
def category_list(request):
    categories = Category.objects.all().order_by('id')
    return render(request, 'dashboard/category_list.html', {'categories': categories})




@superuser_required
def users_list(request):
    users = CustomUser.objects.all().order_by('date_joined')
    online_user_ids = get_online_user_ids()

    for user in users:
        user.is_online = user.id in online_user_ids

    return render(request, 'dashboard/users_list.html', {
        'users': users
    })




@superuser_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)  # user رو پاس بده
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'پست با موفقیت ایجاد شد.')
            return redirect('post_list')
    else:
        form = PostForm(user=request.user)  # user رو پاس بده
    return render(request, 'dashboard/post_form.html', {'form': form, 'title': 'ایجاد پست جدید'})




@superuser_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'پست با موفقیت به‌روزرسانی شد.')
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'dashboard/post_form.html', {'form': form, 'title': 'ویرایش پست'})





@superuser_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'پست حذف شد.')
        return redirect('post_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': post, 'title': 'حذف پست'})




@superuser_required
def create_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'پکیج با موفقیت ایجاد شد.')
            return redirect('package_list')
    else:
        form = PackageForm()
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'ایجاد پکیج جدید'})



@superuser_required
def update_package(request, pk):
    package = get_object_or_404(pakages, pk=pk)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'پکیج با موفقیت به‌روزرسانی شد.')
            return redirect('package_list')
    else:
        form = PackageForm(instance=package)
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'ویرایش پکیج'})



@superuser_required
def delete_package(request, pk):
    package = get_object_or_404(pakages, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'پکیج حذف شد.')
        return redirect('package_list')
    return render(request, 'dashboard/confirm_delete_package.html', {'object': package, 'title': 'حذف پکیج'})





@superuser_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته‌بندی با موفقیت ایجاد شد.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'ایجاد دسته‌بندی جدید'})



@superuser_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'دسته‌بندی با موفقیت به‌روزرسانی شد.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'ویرایش دسته‌بندی'})



@superuser_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'دسته‌بندی حذف شد.')
        return redirect('category_list')
    return render(request, 'dashboard/confirm_delete_category.html', {'object': category, 'title': 'حذف دسته‌بندی'})




@superuser_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'کاربر با موفقیت ایجاد شد.')
            return redirect('users_list')
    else:
        form = CustomUserForm()
    return render(request, 'dashboard/user_form.html', {'form': form, 'title': 'ایجاد کاربر جدید'})



@superuser_required
def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'کاربر با موفقیت به‌روزرسانی شد.')
            return redirect('users_list')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'dashboard/user_form.html', {'form': form, 'title': 'ویرایش کاربر'})



@superuser_required
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'کاربر حذف شد.')
        return redirect('users_list')
    return render(request, 'dashboard/confirm_delete_user.html', {'object': user, 'title': 'حذف کاربر'})



@superuser_required
def activate_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = True
    user.save()
    messages.success(request, 'کاربر فعال شد.')
    return redirect('users_list')



@superuser_required
def deactivate_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = False
    user.save()
    messages.success(request, 'کاربر غیرفعال شد.')
    return redirect('users_list')


