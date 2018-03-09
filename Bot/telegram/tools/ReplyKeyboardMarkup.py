import json
from . HelpClasses import Keyboard


class ReplyKeyboardMarkup(Keyboard):
    def __init__(self, **kwargs):
        self._keyboard = {"keyboard": [[]], 'resize_keyboard': True, **kwargs}
        self._keyboard_type = 'keyboard'
        self._row = 0


def keyboard_remove(yes_no, **kwargs):
    return json.dumps({'remove_keyboard': yes_no, **kwargs})

def make_reply_buttons(buttons):
    kb = ReplyKeyboardMarkup()

    for b in buttons:
        if b[0] == '\n':
            kb.add_par()
            kb.add_button(b[1:])
        elif b[-1] == '\n':
            kb.add_button(b[:-1])
            kb.add_par()
        else:
            kb.add_button(b)
    return kb.json
