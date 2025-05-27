from django.http import HttpResponse
from django.contrib import messages
from blog.forms import ContactMessageForm
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post,ContactMessage
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index_View(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')[:3]

    recent_messages = ContactMessage.objects.order_by('-id')[:5]

    context = {
        'posts': posts,
        'recent_messages': recent_messages,
    }
    return render(request, 'index.html', context)


def about_View(request):

    return render(request, 'about.html')




def blog_view(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date')



    for post in posts:
        post.counted_view += 1  
        post.save(update_fields=['counted_view'])

    return render(request, 'blog.html', {'posts': posts})



def post_detail_View(request, id):

    posts = list(Post.objects.filter(published_date__lte=timezone.now(), status=True).order_by('-published_date'))

    current_post = get_object_or_404(Post, id=id)

    current_post.counted_view += 1
    current_post.save(update_fields=['counted_view'])


    previous_post = None
    next_post = None

    for i, post in enumerate(posts):
        if post.id == current_post.id:
            if i > 0:  
                previous_post = posts[i-1]
            if i < len(posts) - 1:  
                next_post = posts[i+1]
            break

    context = {
        'post': current_post,
        'previous_post': previous_post,
        'next_post': next_post,
    }

    return render(request, 'post_detail.html', context)





def contact_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to send a message.')
            return redirect('blog:contact')

        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.name = request.user.get_full_name() or request.user.username
            message.email = request.user.email
            message.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('blog:contact')
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
            form = ContactMessageForm(initial=initial_data)
        else:
            form = ContactMessageForm()

    recent_messages = ContactMessage.objects.order_by('-id')[:10]

    return render(request, 'contact.html', {
        'form': form,
        'recent_messages': recent_messages,
    })



def packages_View(request):

    return render(request, 'packages.html')

def services_View(request):

    return render(request, 'services.html')







def coming_soon(request):
    html = """
    <html>
        <head>
            <title>Coming Soon</title>
            <style>
                body {
                    background-color: #f4f4f4;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding-top: 150px;
                }
                h1 {
                    font-size: 48px;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>به زودی در دسترس خواهد بود</h1>
        </body>
    </html>
    """
    return HttpResponse(html)

