import sys
import importlib
import traceback

class PluginLoader(object):
    def __init__(self):
        self.plugin_module = [ 'ToPCLI', 'plugin' ]

    def load(self, args):
        base = self.plugin_module + [ args[1] ]
        plugin = base + [ args[2] ]
        plugin_args = args[3:]

        try:
            base = importlib.import_module('.'.join(base))
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            print('Unknown command "%s"' % args[1])
            sys.exit(1)
        base.run_plugin(plugin, plugin_args)
