from ToPCLI.Todoist import Todoist, PRIORITY_TO_LEVEL
import argparse
import sys

def get_args(args):
    parser = argparse.ArgumentParser(prog='todoist tasks complete',
                                     description='Complete task(s).')
    parser.add_argument('ids', nargs='+', type=str, metavar='ID',
                        help='Perform the action on the given ID(s).')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--revert', action='store_true',
                       help='Uncomplete the given task(s) instead.')
    group.add_argument('--archive', '-a', action='store_true',
                       help='Archive the given task(s).')

    return parser.parse_args(args)

def run(args):
    args = get_args(args)

    action = 'complete'
    if args.revert:
        action = 'uncomplete'
    if args.archive:
        action = list(action)
        action.append('archive')

    todoist = Todoist()
    todoist.batch_mode_is(True)

    for id in args.ids:
        if type(action) == list:
            for act in action:
                todoist.do('items', act, id)
        else:
            todoist.do('items', action, id)

    todoist.batch_mode_is(False)
