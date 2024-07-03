import os
from .common import *

INSTALLED_APPS += ["taiga_contrib_proxy_auth"]
PROXY_USERNAME_FIELD = os.getenv("PROXY_USERNAME_FIELD", "X-PROXY-USER")
PROXY_FULLNAME_FIELD = os.getenv("PROXY_FULLNAME_FIELD", "X-PROXY-NAME")
PROXY_EMAIL_FIELD = os.getenv("PROXY_EMAIL_FIELD", "X-PROXY-EMAIL")
