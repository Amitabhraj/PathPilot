from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    """
    Custom decorator that redirects to 'login' if the user is not authenticated.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to the named URL 'login'
            return redirect('user-login') 
        
        # If authenticated, proceed to the actual view
        return view_func(request, *args, **kwargs)
        
    return _wrapped_view