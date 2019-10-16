# Tasks Commands

This design document will detail every command that will be supported by the
provided `tasks` base. This will encompass all actions that modify tasks.

## `tasks create`

Command syntax:
```
todoist tasks create [options] <content>
```
With no options, the task creation will behave the same way as the default add
on Todoist, under the "Inbox" project, with no due date or labels.

The following options will be available:
- `--project`: add the task under the given project ID. This option cannot be
  stacked.
- `--parent`: add the task as a child of the given task ID.
- `--label`: add the task with the given label ID. This option can be stacked.
- `--date`: use the following due date, from the API documentation date formats
  can be:
  - Full-day dates (like “1 January 2018” or “tomorrow”).
  - Floating due dates with time (like “1 January 2018 at 12:00” or “tomorrow at
    10am”).
  - Due dates with time and fixed timezone (like “1 January 2018 at 12:00
    America/Chicago” or “tomorrow at 10am Asia/Jakarta”).

  In addition, any of these due dates can be set to recurring or not, depending
  on the date string, provided by the client.

  This option cannot be stacked.

## `tasks edit`

Command syntax:
```
todoist tasks edit <taskID> [options] [content]
```
With no options, the command will edit the task with the given content. If
absolutely no arguments are given, the command will do nothing.

The following options will be available:
- `--project`: change the task to be under the given project ID.
- `--parent`: change the task to be the child of the given task ID.
- `--add-label`: add the given label ID to the task.
- `--rm-label`: remove the given label ID from the task.
- `--date`: change the due date of the task. If `0` is given, remove the task's
  due date.

## `tasks complete`

Command syntax:
```
todoist tasks complete [--revert|--archive] ID [ID...]
```

This option completes the given task IDs. If the `--revert` option is given, the
task will be uncompleted. If the `--archive` option is given, the task will be
completed and archived.

## `tasks archive`

Command syntax:
```
todoist tasks archive [--revert] ID [ID...]
```
This option will archive the given task IDs. If the `--revert` option is given,
the task will be unarchived instead.
