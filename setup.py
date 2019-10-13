#!/usr/bin/env python3

import os
import sys
from setuptools import setup, find_packages

def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

if sys.version_info < (3, 5):
    die("Need Python >= 3.5; found {}".format(sys.version))

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    reqs = [line.strip() for line in f]

setup(
    name='todoist-cli',
    version='0.0.1',
    description='Todoist command-line interface',
    author='Andrew Tran',
    author_email='andremail03@gmail.com',
    url='https://github.com/NAndLib/todoist-plugable-cli/',
    packages=find_packages(),
    entry_points = { "console_scripts": "todoist=ToPCLI:main" },
    install_requires=reqs,
    )
