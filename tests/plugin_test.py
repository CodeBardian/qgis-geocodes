from qgis.utils import iface, plugins, startPlugin, unloadPlugin

from GeocodeTools import classFactory


def setup_module(module):
    plugins['GeocodeTools'] = classFactory(iface)
    assert plugins['GeocodeTools']


class TestPlugin:

    def test_installation(self):
        assert startPlugin('GeocodeTools')
        actions = plugins['GeocodeTools'].actions
        assert actions

        for action in actions:
            action.trigger()

    def test_unload(self):
        actions = plugins['GeocodeTools'].actions
        assert actions

        plugins['GeocodeTools'].unload()

        assert not plugins['GeocodeTools'].actions

