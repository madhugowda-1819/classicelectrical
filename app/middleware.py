# classicelectricals/middleware.py
import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

class SessionIdleTimeout:
    """Middleware to logout after SESSION_COOKIE_AGE seconds of inactivity."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply if admin is logged in
        if request.session.get('id'):  # the session key you set on login
            now = datetime.datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed = (now - datetime.datetime.fromisoformat(last_activity)).total_seconds()
                if elapsed > settings.SESSION_COOKIE_AGE:
                    request.session.flush()
                    messages.info(request, "Your session expired due to inactivity.")
                    return redirect('admin/adminlogin')  # name of your login view

            # Update last_activity timestamp
            request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
