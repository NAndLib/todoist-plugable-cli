import sys
import importlib
import traceback

def run_plugin(plugin, args):   
    try:
        plugin_mod = importlib.import_module('.'.join(plugin))
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        print('Failed to run command "%s"' % plugin[-1])
        sys.exit(1)

    plugin_mod.run(args)
