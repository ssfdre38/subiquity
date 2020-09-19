# Copyright 2015 Canonical, Ltd.
#
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

import attr

from subiquitycore.context import with_context

from subiquity.common.types import IdentityData
from subiquity.controller import SubiquityTuiController
from subiquity.ui.views import IdentityView

log = logging.getLogger('subiquity.controllers.identity')


class IdentityController(SubiquityTuiController):

    autoinstall_key = model_name = "identity"
    autoinstall_schema = {
        'type': 'object',
        'properties': {
            'realname': {'type': 'string'},
            'username': {'type': 'string'},
            'hostname': {'type': 'string'},
            'password': {'type': 'string'},
            },
        'required': ['username', 'hostname', 'password'],
        'additionalProperties': False,
        }

    def load_autoinstall_data(self, data):
        if data is not None:
            identity_data = IdentityData(
                realname=data.get('realname', ''),
                username=data['username'],
                hostname=data['hostname'],
                crypted_password=data['password'],
                )
            self.model.add_user(identity_data)

    @with_context()
    async def apply_autoinstall_config(self, context=None):
        if not self.model.user:
            if 'user-data' not in self.app.autoinstall_config:
                raise Exception("no identity data provided")

    def make_ui(self):
        data = IdentityData()
        if self.model.user is not None:
            data.username = self.model.user.username
            data.realname = self.model.user.realname
        if self.model.hostname:
            data.hostname = self.model.hostname
        return IdentityView(self, data)

    def run_answers(self):
        if all(elem in self.answers for elem in
               ['realname', 'username', 'password', 'hostname']):
            identity = IdentityData(
                realname=self.answers['realname'],
                username=self.answers['username'],
                hostname=self.answers['hostname'],
                crypted_password=self.answers['password'])
            self.done(identity)

    def cancel(self):
        self.app.prev_screen()

    def done(self, identity_data):
        log.debug(
            "IdentityController.done next_screen user_spec=%s",
            identity_data)
        self.model.add_user(identity_data)
        self.configured()
        self.app.next_screen()

    def make_autoinstall(self):
        if self.model.user is None:
            return {}
        r = attr.asdict(self.model.user)
        r['hostname'] = self.model.hostname
        return r
