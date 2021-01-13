from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fun(request, *args, **kwargs)

    return wrapper_fun

def allowed_users(allowed_roles=[]):
    def decorator(view_fun):
        def wrapper_fun(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_fun(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_fun
    return decorator

def admin_only(view_fun):
    def wrapper_function(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group == 'customer':
                return redirect('user-page')

            if group == 'admin':
                return view_fun(request, *args, **kwargs)
            else:
                return redirect('user-page')
    return wrapper_function
