from ToPCLI.PluginLoader import PluginLoader
import sys

loader = PluginLoader()

loader.load(sys.argv)
