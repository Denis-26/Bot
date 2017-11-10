import json
from . HelpClasses import Keyboard


class ReplyKeyboardMarkup(Keyboard):
    def __init__(self):
        self._keyboard = {"keyboard": [[]], 'resize_keyboard': True}
        self._keyboard_type = 'keyboard'
        self._row = 0


def keyboard_remove(yes_no, **kwargs):
    return json.dumps({'remove_keyboard': yes_no, **kwargs})
