from config import token
from datetime import datetime
import sys
import webbrowser
import hashlib
import todoist

class Todoist(object):
    def __init__(self):
        self.api = todoist.api.TodoistAPI(token)

    def _reader(func):
        def sync_run(self, *args, **kwargs):
            self.api.sync()
            return func(self, *args, **kwargs)
        return sync_run

    def _writer(func):
        def sync_run_commit(self, *args, **kwargs):
            self.api.sync()
            result = func(self, *args, **kwargs)
            if not result:
                print("Function failed to execute, not commiting request.",
                      file=sys.stderr)
            else:
                self.api.commit()
            return result
        return sync_run_commit
    
    @_reader
    def get_state(self, item=None, *ids):
        """
        Returns a dictionary of the current state, keyed by ID.
        - item: return the state of this specific item.
        - ids: only return objects matching the given ids.

        If no item is provided, the entire state is returned. Not keyed by ID.
        """
        if not item and not properties:
            return self.api.state

        objs = self.api.state[item]
        data = {}

        for obj in objs:
            if ids and not obj['id'] in ids:
                continue
            data[obj['id']] = obj

        return data if data else self.api.state

    @_writer
    def add(self, type, content, **kwargs):
        """
        Add/Create a "type" object with "name".
        - type: the type of object in Todoist. Types can be: projects, items,
          notes, project_notes, labels, and reminders.
        - content: the content of the object to be created.
        """
        cmd_type = getattr(self.api, type)
        cmd = getattr(cmd_type, "add")

        return cmd(content, **kwargs)
