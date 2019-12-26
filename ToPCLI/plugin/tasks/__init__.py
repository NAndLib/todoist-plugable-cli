import sys
import importlib
import traceback

description = 'Commands related to editing/updating tasks'

def run_plugin(plugin, args):
    plugin = importlib.import_module('.'.join(plugin))

    plugin.run(args)
