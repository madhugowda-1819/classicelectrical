from django.shortcuts import redirect

def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('id') is None:
            return redirect('adminlogin')
        return view_func(request, *args, **kwargs)
    return wrapper
