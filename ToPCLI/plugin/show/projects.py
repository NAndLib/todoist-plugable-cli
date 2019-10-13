from ToPCLI.Todoist import Todoist, CodeToColors
import argparse
import re

todoist = None

def get_args(args):
    parser = argparse.ArgumentParser(prog='todoist show projects',
                                     description='Show available projects.')
    parser.add_argument('regex', nargs='?', default='.*',
                        help='Only show projects matching "regex".')
    parser.add_argument('--parent', '-p', action='store_true',
                        help='Show ID and name of parent project.')
    parser.add_argument('--color', '-C', action='store_true',
                        help='Show color of project.')

    return parser.parse_args(args)

def print_projects(projects, regex, header):
    data = [ header ]
    for project in projects:
        if re.match(regex, project['name']):
            info = []
            has_parent = project['parent_id'] is not None
            for item in header:
                if item == 'parent_name':
                    if not has_parent:
                        info.append('None')
                    else:
                        parent_project = \
                            todoist.get_by_id('projects', project['parent_id'])
                        info.append(parent_project['name'])
                elif item == 'color':
                    info.append(CodeToColors[project[item]])
                else:
                    info.append(str(project[item]))
            data.append(tuple(info))
    format_str = "{:<15}" * len(header)
    for item in data:
        print(format_str.format(*item))

def run(args):
    global todoist
    args = get_args(args)

    todoist = Todoist()
    projects = todoist.get_state('projects')

    todoist.batch_mode_is(True)
    header = [ 'id', 'name' ]
    if args.parent:
        header += [ 'parent_id', 'parent_name' ]
    if args.color:
        header += [ 'color' ]

    print_projects(projects, args.regex, header)
    todoist.batch_mode_is(False)
