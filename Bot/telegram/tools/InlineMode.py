import json
from . HelpClasses import Keyboard, Get


class InlineQueryResultPhoto(Get):
    def __init__(self, i_d, photo_url, thumb_url, **kwargs):
        self._info = {**kwargs, **{'type': 'photo', 'photo_url': photo_url, 'thumb_url': thumb_url, 'id': i_d}}


class InlineQueryResultArticle(Get):
    def __init__(self, i_d, title, input_message_content, **kwargs):
        self._info = {**kwargs, **dict(type='article', title=title,
                                       input_message_content=json.dumps(input_message_content), id=i_d)}


class InlineKeyboardMarkup(Keyboard):
    def __init__(self):
        self._keyboard = {"inline_keyboard": [[]]}
        self._row = 0
        self._keyboard_type = 'inline_keyboard'


class InputTextMessageContent(Get):
    def __init__(self, message_text, **kwargs):
        self._info = kwargs
        self._info['message_text'] = message_text


class AnswerInlineQuery(Get):
    def __init__(self, inline_query_id, results, **kwargs):
        self._info = {**kwargs, **{'inline_query_id': inline_query_id, 'results': json.dumps(results)}}


def make_inline_buttons(buttons, cb_data):
    kb = InlineKeyboardMarkup()

    for b, cb in zip(buttons, cb_data):
        if b[0] == '\n':
            kb.add_par()
            kb.add_button(b[1:], callback_data = cb)
        elif b[-1] == '\n':
            kb.add_button(b[:-1], callback_data = cb)
            kb.add_par()
        else:
            kb.add_button(b, callback_data=cb)
    return kb.json
