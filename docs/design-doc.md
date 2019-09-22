# Todoist Plugable Command Line Interface (ToPCLI)

## Introduction

### Todoist
[Todoist](https://todoist.com/) is a task manager and orgnazier created by
Doist. It provides an abundance of features to help manage and organize tasks
such as projects, labels, priority levels, and so on. I use it extensively for
every day tassk from anywhere to chores to work.

### The API

The Doist team has graciously provided a [Python
API](https://github.com/doist/todoist-python) to that provides a Python
programable way to interact with their [REST
API](https://developer.todoist.com/sync/v8/#summary-of-contents). This will be
the main library used by this project.

### Reason and Goal

The current biggest todoist CLI tool available right now is
[sachaos/todoist](https://github.com/sachaos/todoist). The app provides
implemtation for all basic Todoist functionality. However, the application is
limited to just the given functionality and there is no good way to extend its
functionality beyond what is provided.

The goal of this project is to to create a commandline interface for Todoist
that is fully plugable. That is, the application will be built with the idea
that anyone can extend its functionality to do whatever they want easily by
providing compatible plugin modules.

## Overview

### Plug-in Architecture

The application will attempt to follow a plugin-oriented architecture. That is,
there will be a single core system whose purpose is to expose the current
Todoist API in a scriptable/hookable way such that plug-in modules can easily
be programmed and linked to the application.

The core system will have the following requirements:
- Make it easier to perform basic Todoist tasks through scriptable commands.
  This will be done by extending on the Todoist Python API.
- Be able to load/unload plugins automatically without manual prompting.

While the core system will provide a quicker way to interface with the API, all
commands that actually perform any tasks will be added through plugins. This
means that in an ideal situation, the user will not have to interact with the
core system at all.

### Plugin Structure

There will be two ways to extend ToPCLI: adding a plugin base with plugins or
adding plugins to an existing plugin base.

A plugin base can be seen as a catergory of functionality while a plugin is the
functionality itself.

For example, a plugin base could be "Tasks", and plugins within that base could
be "Edit Task", "Add Task", "Create Task", etc.

The following plugin bases are provided by default:
- Tasks: all plugins that performs any tasks actions.
- Projects: all plugins that performs any project actions.
- Labels: all plugins that performs any label actions.
- Show: all plugins that shows infomration about the current Todoist state.
- Auto: all plugins that are meant to be run continiously for scripts or
  cronjobs.

The plugin bases are not hard-and-fast rules, merely a way to keep things
organized. It is up to the user to determine which base their plugin should go
into. If needed, the user can also provide their own plugin base.

Some plugins are also provided by default to each base to allow basic Todoist
functionality:
- Tasks: Create, edit, complete, archive, delete, label, add to project,
  priotize, set parent/child, set/reschedule duedate.
- Projects: create, edit, delete, archive, set parent/child.
- Labels: create, edit, delete.
- Show: show all tasks, projects, labels; show tasks in project, with label,
  due on date; show tasks with priority.

This design will hopefully keep the application extensible while also being
defined enough right out of the box.

## Implementation

Every ToPCLI command will have the following form:
```
todoist <plugin-base> <command>
```
Where `<plugin-base>` is the name of any available plugin bases and `<command>`
will be the name of the plugin that the user wants to run. See [plugin
base](plugin-base) and [plugins](plugins) for more detailed explanations of how
this will work.

### Core system

The core system will be split into two parts: the Todoist API extension and the
plugin loader.

#### Todoist API Extension

#### Plugin Loader

The plugin loader will run everytime any `todoist` command is issued. The loader
will then do a search through the the application's `plugins` directory to load
the specific plugin base and, subsequently, the plugin that matches the command
given.

The loader will look for an `__init__.py` file within the plugin base that it is
loading.

### Plugin Bases

Any python module under the application's `plugin` directory with a valid
`__init__.py` file will be recognized as a plugin base by ToPCLI.

The plugin base will have the following responsibilities:
- List itself as a valid argument for the top level argument parser.
- List all valid Python files under it as valid plugins and as arguments for the
  sub-level argument parser.
- List all valid Python modules under it as valid plugins and arguments for the
  sub-level arguemnt parser.
- Provide correct argument handlers to all of the plugins listed under it.

### Plugins

A plugin can be a Python file or a Python module under a plugin base directory.
The filename or module name will be command that is enabled for that specific
plugin base.

For example, the plugin file `tasks/edit.py` would enable the command: `todoist
tasks edit ...` and the plugin module `tasks/label` would enable the command:
`todoist tasks label ...`.

For the plugin base to correctly provide handlers for any plugin listed, a
plugin must have a `run(args)` function defined, where `args` is a list of of
arguments that it will get from the plugin base.

## Testing
