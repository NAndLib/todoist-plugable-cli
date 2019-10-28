from config import token
from contextlib import contextmanager
import sys
import todoist

CODE_TO_COLORS = {
    30 : 'BERRY_RED',
    31 : 'RED',
    32 : 'ORANGE',
    33 : 'YELLOW',
    34 : 'OLIVE_GREEN',
    35 : 'LIME_GREEN',
    36 : 'GREEN',
    37 : 'MINT_GREEN',
    38 : 'TEAL',
    39 : 'SKY_BLUE',
    40 : 'LIGHT_BLUE',
    41 : 'BLUE',
    42 : 'GRAPE',
    43 : 'VIOLET',
    44 : 'LAVENDER',
    45 : 'MAGENTA',
    46 : 'SALMON',
    47 : 'CHARCOAL',
    48 : 'GREY',
    49 : 'TAUPE',
}

COLORS_TO_CODE = {
    'BERRY_RED' : 30,
    'RED' : 31,
    'ORANGE' : 32,
    'YELLOW' : 33,
    'OLIVE_GREEN' : 34,
    'LIME_GREEN' : 35,
    'GREEN' : 36,
    'MINT_GREEN' : 37,
    'TEAL' : 38,
    'SKY_BLUE' : 39,
    'LIGHT_BLUE' : 40,
    'BLUE' : 41,
    'GRAPE' : 42,
    'VIOLET' : 43,
    'LAVENDER' : 44,
    'MAGENTA' : 45,
    'SALMON' : 46,
    'CHARCOAL' : 47,
    'GREY' : 48,
    'TAUPE' : 49,
}

PRIORITY_TO_LEVEL = {
    'p1' : 4,
    'p2' : 3,
    'p3' : 2,
    'p4' : 1
}

LEVEL_TO_PRIORITY = {
    4 : 'p1',
    3 : 'p2',
    2 : 'p3',
    1 : 'p4'
}

class Todoist(object):
    def __init__(self, batch_mode=False):
        self.api = todoist.api.TodoistAPI(token)
        self._batch_mode = batch_mode

    def _sync(self):
        """
        Only sync if batch_mode is False.
        """
        if self._batch_mode:
            return
        self.api.sync()

    def _commit(self):
        """
        Only commit if batch_mode is False.
        """
        if self._batch_mode:
            return
        self.api.commit()

    def _reader(func):
        def sync_run(self, *args, **kwargs):
            self._sync()
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                print("Failed to run command.", file=sys.stderr)
                print(e)
                sys.exit(1)
            return result
        return sync_run

    def _writer(func):
        def sync_run_commit(self, *args, **kwargs):
            self._sync()
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                print("Failed to run command.", file=sys.stderr)
                print(e)
                sys.exit(2)
            self._commit()
            return result
        return sync_run_commit

    def _get_cmd(self, type, command):
        """
        Gets the correct command for the specified type.
        """
        cmd_type = getattr(self.api, type)
        return getattr(cmd_type, command)

    def batch_mode_is(self, state):
        """
        Sync and commit changes before toggling batch_mode
        """
        self.api.sync()
        self.api.commit()
        self._batch_mode = state

    @contextmanager
    def batch_mode(self):
        self.batch_mode_is(True)
        yield
        self.batch_mode_is(False)

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
        else:
            return self.api.state[item]

    def _action_by_id(self, type, action, id, **kwargs):
        """
        Perform the "type" "action" on the given id with the given args.
        - type: api action types, can be projects, items, labels, quick, etc.
        - action: the action to perform, can be complete, update, archive,
          etc.
        - id: the id of the object.
        - kwargs: arguments for the action to run.
        """
        cmd = self._get_cmd(type, action)

        return cmd(id, **kwargs)

    @_reader
    def read_action_by_id(self, type, action, id, **kwargs):
        """
        Perform "action" of "type" with the the given "id"
        - type: the type of object in Todoist.
        - action: the action to perform, e.g., get, get_data, etc.
        - id: the target id.
        """
        return self._action_by_id(type, action, id, **kwargs)

    @_writer
    def write_action_by_id(self, type, action, id, **kwargs):
        """
        Perform "action" of "type" with the the given "id"
        - type: the type of object in Todoist.
        - action: the action to perform, e.g., get, get_data, etc.
        - id: the target id.
        """
        return self._action_by_id(type, action, id, **kwargs)

    @_writer
    def add(self, type, content, **kwargs):
        """
        Add/Create a "type" object with "content".
        - type: the type of object in Todoist. Types can be: projects, items,
          notes, project_notes, labels, and reminders.
        - content: the content of the object to be created.
        - **kwargs: appropriate keyword args for the type.
        """
        return self._get_cmd(type, 'add')(content, **kwargs)
