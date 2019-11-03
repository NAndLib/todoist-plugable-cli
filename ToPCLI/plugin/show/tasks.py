from ToPCLI.Todoist import Todoist
import argparse
import re

todoist = None

def get_args(args):
    parser = argparse.ArgumentParser(prog='show tasks',
                                     description='Show available tasks.')
    parser.add_argument('regex', nargs='?', default='.*',
                        help='Only show tasks matching "regex".')
    parser.add_argument('--id', '-i', metavar='ID', type=int,
                        help='Show details of the task with the given ID.')
    parser.add_argument('--projectRE', '-pre', metavar='REGEX', type=str,
                        help='Show tasks with the matching projects regex.')
    parser.add_argument('--labelRE', '-lre', metavar='REGEX', type=str,
                        help='Show tasks with the matching labels regex.')
    parser.add_argument('--date', '-d', metavar='DATE', type=str,
                        help='Show tasks with matching due date.')
    parser.add_argument('--ordered', '-o', action='store_true',
                        help='Show tasks ordered by \
                              parent-child relationships.')

    return parser.parse_args(args)

def run(args):
    global todoist
    args = get_args(args)

    todoist = Todoist()
