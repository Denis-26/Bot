import json


class Get:
    def __getattr__(self, attr):
        return self._info if attr == 'json' else None


class Keyboard:
    def add_par(self):
        self._keyboard[self._keyboard_type].append([])
        self._row += 1

    def add_button(self, text, **kwargs):
        self._keyboard[self._keyboard_type][self._row].append({'text': text, **kwargs})

    def __getattr__(self, attr):
        return json.dumps(self._keyboard) if attr == 'json' else None
