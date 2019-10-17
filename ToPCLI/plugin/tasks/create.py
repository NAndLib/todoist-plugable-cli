from ToPCLI.Todoist import Todoist, PRIORITY_TO_LEVEL
import argparse
import sys

def get_args(args):
    parser = argparse.ArgumentParser(prog='tasks create',
                                     description='Create a new task.')
    parser.add_argument('content', type=str, metavar='CONTENT',
                        help='The content of the task. Must a single string')
    parser.add_argument('--project', '-p', type=str, metavar='ID',
                        help='Add the task under the project ID.')
    parser.add_argument('--parent', '-P', type=str, metavar='ID',
                        help='Make the task with the given ID \
                              a parent of this task')
    parser.add_argument('--priority', '-pr', type=str, metavar='PRIORITY',
                        help='Set the task\'s priority. Can be p1 to p4.')
    parser.add_argument('--label', '-l', type=str,
                        metavar='ID', action='append',
                        help='Add the given label ID to the task. \
                              Can be given multiple times')
    date_help='''
    DATE can be:
    - Full-day dates (like "1 January 2018" or "tomorrow").
    - Floating due dates with time (like "1 January 2018 at 12:00" or "tomorrow
      at 10am").
    - Recurring dates (like "every day" or "every other day").
    '''
    parser.add_argument('--date', '-d', type=str, metavar='DATE',
                        help=date_help)

    return parser.parse_args(args)

def run(args):
    args = get_args(args)

    todoist = Todoist()
    item = {}

    if args.project:
        item['project_id'] = args.project
    if args.date:
        item['due'] = args.date
    if args.priority:
        if args.priority not in PRIORITY_TO_LEVEL:
            print('Priority can only be p1 to p4.', file=sys.stderr)
            sys.exit(1)
        item['priority'] = PRIORITY_TO_LEVEL[args.priority]
    if args.parent:
        item['parent_id'] = args.parent
    if args.label:
        item['labels'] = args.label

    todoist.add('items', args.content, **item)
