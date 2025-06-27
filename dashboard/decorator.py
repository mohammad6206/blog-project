from django.shortcuts import redirect, render
from functools import wraps

def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # اگر لاگین نکرده بود
        elif not request.user.is_superuser:
            return render(request, '403.html', status=403)  # اگر سوپر یوزر نبود
        return view_func(request, *args, **kwargs)
    return wrapper
