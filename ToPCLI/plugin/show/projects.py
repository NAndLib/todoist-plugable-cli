from ToPCLI.Todoist import Todoist, CodeToColors
import argparse
import re

todoist = Todoist()

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

def print_projects(projects, regex, extra_info):
    header = ('id', 'name') + tuple(extra_info)
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
    projects = todoist.get_state('projects')

    args = get_args(args)
    extra_info = []
    if args.parent:
        extra_info += [ 'parent_id', 'parent_name' ]
    if args.color:
        extra_info += [ 'color' ]

    print_projects(projects, args.regex, extra_info)
