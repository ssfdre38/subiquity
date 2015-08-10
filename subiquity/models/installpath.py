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
from subiquity.model import ModelPolicy


log = logging.getLogger("subiquity.models.installpath")


class InstallpathModel(ModelPolicy):
    """ Model representing install options

    List of install paths in the form of:
    ('UI Text seen by user', <signal name>, <callback function string>)
    """
    prev_signal = ('Back to welcome screen',
                   'welcome:show',
                   'welcome')

    signals = [
        ('Install Path View',
         'installpath:show',
         'installpath')
    ]

    install_paths = [('Install Ubuntu',
                      'installpath:ubuntu',
                      'install_ubuntu'),
                     ('Install MAAS Region Server',
                      'installpath:maas-region-server',
                      'install_maas_region_server'),
                     ('Install MAAS Cluster Server',
                      'installpath:maas-cluster-server',
                      'install_maas_cluster_server'),
                     ('Test installation media',
                      'installpath:test-media',
                      'test_media'),
                     ('Test machine memory',
                      'installpath:test-memory',
                      'test_memory')]

    def get_signal_by_name(self, selection):
        for x, y, z in self.get_signals():
            if x == selection:
                return y

    def get_signals(self):
        return self.signals + self.install_paths

    def get_menu(self):
        return self.install_paths
