DEBUG=True
CSRF_ENABLED=True
SECRET_KEY="please_override_me_in_localsettings.py"
CSRF_SESSION_LKEY="please_override_me_in_localsettings.py"

# Import local settings
try:
    from localsettings import *
except ImportError:
    pass
