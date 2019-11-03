from ToPCLI.Todoist import Todoist, CODE_TO_COLORS, LEVEL_TO_PRIORITY
from ToPCLI.Helper import Table
import argparse
import re

todoist = None

def get_args(args):
    parser = argparse.ArgumentParser(prog='todoist show projects',
                                     description='Show available projects.')
    parser.add_argument('regex', nargs='?', type=str,
                        help='Only show projects matching "regex".')
    parser.add_argument('--id', '-i', metavar='ID', type=int,
                        help='Show details of the project with the given ID')
    parser.add_argument('--parent', '-p', action='store_true',
                        help='Show ID and name of parent project.')
    parser.add_argument('--color', '-C', action='store_true',
                        help='Show color of project.')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='Show item counts.')

    return parser.parse_args(args)

def get_parent_project(todoist, project):
    parent = None
    if project['parent_id'] is not None:
        parent_id = project['parent_id']
        parent = todoist.read_action_by_id('projects',
                                           'get', parent_id)['project']
    return parent

def build_table_from_id(id, table):
    project_data = todoist.read_action_by_id('projects',
                                             'get_data', id)
    project = project_data['project']
    items = project_data['items']

    table.header_is(["{}:".format(project['name'])])
    parent = get_parent_project(todoist, project)
    if parent is not None:
        table.add_row(['Parent:', parent['name'], parent['id']])

    table.add_row(['Color:', CODE_TO_COLORS[project['color']]])
    table.add_row(['Items:'])
    items_header = ['ID', 'Priority', 'Due Date', 'Labels', 'Content']
    table.add_row(items_header)

    # Print items in order of priority
    for item in sorted(items, key=lambda i: i['priority']):
        item_row = []
        item_row.append(item['id'])
        item_row.append(LEVEL_TO_PRIORITY[item['priority']])
        if item['due']:
            item_row.append(item['due']['string'])
        else:
            item_row.append(' ')

        labels = []
        for label_id in item['labels']:
            label = todoist.read_action_by_id('labels',
                                              'get_by_id', label_id)
            labels.append(label['name'])
        item_row.append(', '.join(labels))
        item_row.append(item['content'])

        table.add_row(item_row)

def build_table_from_args(args, table):
    projects_state = todoist.get_state('projects')

    header = [ 'ID', 'Name' ]
    if args.parent:
        header.append('Parent (ID)')
    if args.color:
        header.append('Color')
    if args.summary:
        header.append('Item count')
    table.header_is(header)

    for project in projects_state:
        if args.regex:
            if not re.match(args.regex, project['name']):
                continue

        project_row = []
        project_row.append(project['id'])
        project_row.append(project['name'])

        if args.parent:
            parent = get_parent_project(todoist, project)
            if parent is not None:
                project_row.append("{} ({})".format(parent['name'],
                                                    parent['id']))
            else:
                project_row.append(" ")
        if args.color:
            project_row.append(CODE_TO_COLORS[project['color']])
        if args.summary:
            items = todoist.read_action_by_id(
                'projects', 'get_data', project['id'])['items']
            project_row.append(len(items))

        table.add_row(project_row)

def run(args):
    global todoist
    args = get_args(args)

    todoist = Todoist()
    with todoist.batch_mode():
        table = Table()

        if args.id:
            build_table_from_id(args.id, table)
        else:
            build_table_from_args(args, table)

        table.render()
