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

import logging
import sys
from django.db import transaction as tx
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from django.apps import apps

from taiga.base.utils.slug import slugify_uniquely
from taiga.base import exceptions as exc
from django.conf import settings
from taiga.auth.services import send_register_email
from taiga.auth.services import make_auth_response_data, get_membership_by_token
from taiga.auth.signals import user_registered as user_registered_signal

from . import connector

PUBLIC_REGISTER_ENABLED = getattr(settings, "PUBLIC_REGISTER_ENABLED", True)

@tx.atomic
def proxy_register(username:str, email:str, full_name:str, token:str=None):
    """
    Register a new user from proxy auth.

    This can raise `exc.IntegrityError` exceptions in
    case of conflicts found.

    :returns: User
    """
    auth_data_model = apps.get_model("users", "AuthData")
    user_model = apps.get_model("users", "User")

    try:
        # proxy user association exists?
        auth_data = auth_data_model.objects.get(key="proxy", value=username)
        user = auth_data.user
    except auth_data_model.DoesNotExist:
        try:
            # Is a user with the same email as the prxoy auth user?
            user = user_model.objects.get(email=email)
            auth_data_model.objects.create(user=user, key="proxy", value=username, extra={})
        except user_model.DoesNotExist:
            if PUBLIC_REGISTER_ENABLED:
                # Create a new user
                username_unique = slugify_uniquely(username, user_model, slugfield="username")
                user = user_model.objects.create(email=email,
                                                username=username_unique,
                                                full_name=full_name)
                auth_data_model.objects.create(user=user, key="proxy", value=username_unique, extra={})

                send_register_email(user)
                user_registered_signal.send(sender=user.__class__, user=user)
            else:
                raise exc.IntegrityError(
                _("Sorry, was unable to locate user and registrations have been disabled by the Administrator"))


    if token:
        membership = get_membership_by_token(token)

        try:
            membership.user = user
            membership.save(update_fields=["user"])
        except IntegrityError:
            raise exc.IntegrityError(_("This user is already a member of the project."))

    return user


def proxy_login_func(request):
    print ("---- Inside proxy login func ----")
    user_info = connector.me(request.headers)
    user = proxy_register(username=user_info.username,
                           email=user_info.email,
                           full_name=user_info.full_name
                          )
    data = make_auth_response_data(user)
    return data


root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
