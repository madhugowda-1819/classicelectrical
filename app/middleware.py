# middleware.py
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings

class SessionIdleTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_path = '/adminlogin/'  # change if your login URL is different
        admin_id = request.session.get('id')

        if admin_id:
            now = timezone.now()
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed = (now - timezone.datetime.fromisoformat(last_activity)).total_seconds()
                if elapsed > settings.SESSION_COOKIE_AGE:
                    request.session.flush()
                    return redirect('adminlogin')
            request.session['last_activity'] = now.isoformat()
        else:
            # Only redirect if not already on login page
            if request.path != login_path and request.path.startswith('/admin'):
                return redirect('adminlogin')

        return self.get_response(request)
