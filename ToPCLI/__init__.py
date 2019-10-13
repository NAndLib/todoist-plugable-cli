from ToPCLI.PluginLoader import PluginLoader
import sys

def main():
    loader = PluginLoader()

    loader.load(sys.argv)
