# Copyright (C) 2014-2017 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2017 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2017 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2017 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json

from collections import namedtuple
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taiga.base.connectors.exceptions import ConnectorBaseException


class ProxyAuthError(ConnectorBaseException):
    pass


######################################################
# Proxy http headers
######################################################

USER_FIELD = getattr(settings, "PROXY_USERNAME_FIELD", "X-PROXY-USER")
NAME_FIELD = getattr(settings, "PROXY_FULLNAME_FIELD", "X-PROXY-NAME")
EMAIL_FIELD = getattr(settings, "PROXY_EMAIL_FIELD", "X-PROXY-EMAIL")

User = namedtuple("User", ["username", "full_name", "email"])

######################################################
# Get user details from http headers
######################################################

def get_user_profile(headers: dict = HEADERS):
    username = None
    full_name = None
    email = None

    if headers.get(USER_FIELD, None) != None :
        username = headers.get(USER_FIELD, None)

    elif headers.get(NAME_FIELD, None) != None :
        full_name = headers.get(NAME_FIELD, None) 

    elif headers.get(EMAIL_FIELD, None) != None :
        email = headers.get(EMAIL_FIELD, None)
    
    if username == None:
        username = email

    user =  User(username=username,
                full_name=full_name,
                email=email)
    return user

######################################################
# Convined calls
######################################################


def me(headers: dict) -> tuple:
    user = get_user_profile(headers=headers)
    return user
