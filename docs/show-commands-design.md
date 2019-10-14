# Design Doc For Each Default Show Commands

Show commands allows users to get an overview of different states of their
Todoist. Each command will provide their own set of filtering abilities along
with an overall `filter` show command that's aimed to work with and extend the
existing Todoist filters.

Show commands will attempt to limit the number of characters per row to 80
characters, although that will not be a hard constraint.

Each show command will have a base, no argument version as well as supporting
extra functionality. Because of this, each show command will be a directory
plugin inside of the `show` base.

There will be three default show commands: `show projects`, `show tasks`, and
`show filtered`. Of course, adding a new show command is simply adding another
module in the `show` base directory.

Because show commands will require significant printing and formatting, a
printer class might be useful.

## `show projects`

This command shows any information related to projects. The default `show
projects` with no arguments will show a list of all projects names along with
their IDs. The projects will be sorted by name.

Extra functionality:
- Show projects matching a REGEX.
- Show projects with the name and ID of their parents.
- Show projects with their colors.
- Show projects and the number of items each of them have.
- Show projects with the given ID. This option will show extra information,
  including:
  - Color.
  - Tasks.
  - Parent.
  - Children.
  - Notes.
  This option will ignore everything other options besides the REGEX one.

## `show tasks`

This command shows information related to tasks. The default `show tasks` with
no arguments will show a list of all uncompleted, non-section tasks with their
IDs, projects, labels, and due date. The tasks list will be sorted in ascending
order of due dates: from most urgent to least urgent, with "No due date." being
the least.

Extra functionality:
- Show tasks matching a REGEX.
- Show tasks with the name and ID of their parents.
- Show tasks under project with name matching REGEX. This command will also show
  the project's ID.
- Show tasks with the specified due date. This command will be quite difficult.
- Show tasks with due dates only. The inverse should also be possible.
- Show ALL tasks, including completed ones and section ones.
- Show tasks with labels matching REGEX.
- Show tasks with the given ID. This option will show extra information,
  including:
  - Color.
  - Children tasks.
  - Project.
  - Labels.
  - Due dates.
  - Notes.

## `show filtered`
