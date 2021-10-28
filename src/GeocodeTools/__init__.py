
try:
    import sys
    sys.path.append("D:/Program Files/JetBrains/PyCharm 2021.2/debug-eggs/pydevd-pycharm.egg")
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=51669, stdoutToServer=True, stderrToServer=True, suspend=False)
except Exception as e:
    pass


def classFactory(iface):
    from GeocodeTools.plugin import GeocodeToolsPlugin
    return GeocodeToolsPlugin(iface)
