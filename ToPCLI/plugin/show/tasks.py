from ToPCLI.Todoist import Todoist, LEVEL_TO_PRIORITY
from ToPCLI.Helper import Table
import argparse
import re

todoist = None

def get_args(args):
    parser = argparse.ArgumentParser(prog='todoist show tasks',
                                     description='Show available tasks.')
    parser.add_argument('regex', nargs='?', default='.*',
                        help='Only show tasks matching "regex".')
    parser.add_argument('--id', '-i', metavar='ID', type=int,
                        help='Show details of the task with the given ID.')
    parser.add_argument('--projectRE', '-pre', metavar='REGEX', type=str,
                        help='Show tasks with the matching projects regex.')
    parser.add_argument('--labelRE', '-lre', metavar='REGEX', type=str,
                        help='Show tasks with the matching labels regex.')
    parser.add_argument('--date-only', '-d', action='store_true',
                        help='Show only tasks with due date.')
    parser.add_argument('--ordered', '-o', action='store_true',
                        help='Show tasks ordered by \
                              parent-child relationships.')

    return parser.parse_args(args)

def build_table_from_args(table, args):
    def project_name(id):
        if not id:
            return None
        project = todoist.get('projects', id)
        return project['name']
    def label_name(id):
        if not id:
            return None
        label = todoist.get('labels', id)
        return label['name']

    filters = [ lambda item: not item['content'].endswith(':')  ]
    filters += [ lambda item: not item['checked'] ]
    filters += [ lambda item: re.match(args.regex, item['content']) ]
    if args.projectRE:
        filters += [ lambda item: re.match(args.projectRE,
                                         project_name(item['project_id'])) ]
    if args.labelRE:
        def match_labels(item):
            for label_id in item['labels']:
                yield re.match(args.labelRE, label_name(label_id))
        filters += [ lambda item: any(match_labels(item)) ]

    table.header_is(['ID', 'Project (ID)', 'Labels (ID)',
                     'Due Date', 'Priority', 'Content'])

    items = todoist.get_state('items')
    for item in filter(lambda item: all([f(item) for f in filters]), items):
        if args.date_only and not item['due']:
            continue
        item_row = []
        item_row.append(item['id'])
        item_row.append('{} ({})'.format(project_name(item['project_id']),
                                         item['project_id']))
        labels_col = []
        for label_id in item['labels']:
            labels_col.append("{} ({})".format(label_name(label_id), label_id))
        item_row.append(', '.join(labels_col))
        item_row.append(item['due']['string'] if item['due'] else None)
        item_row.append(LEVEL_TO_PRIORITY[item['priority']])
        item_row.append(item['content'])

        table.add_row(item_row)

    table.sort('Priority')

def run(args):
    global todoist
    args = get_args(args)

    table = Table()

    todoist = Todoist()
    with todoist.batch_mode():
        if not args.id:
            build_table_from_args(table, args)

    table.render()
