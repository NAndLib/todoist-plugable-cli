import sys
import importlib
import traceback

description = 'Show information about requested objects.'

def run_plugin(plugin, args):
    plugin = importlib.import_module('.'.join(plugin))

    plugin.run(args)
