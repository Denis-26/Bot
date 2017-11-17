from .Types import Update
import logging

def parser(update):
    try:
        return Update(
            update['update_id'],
            update.get('message', None),
            update.get('edited_message', None),
            update.get('channel_post', None),
            update.get('edited_channel_post', None),
            update.get('inline_query', None),
            update.get('chosen_inline_result', None),
            update.get('callback_query', None),
            update.get('shipping_query', None),
            update.get('pre_checkout_query', None)
        )
    except Exception as ex:
        logging.error("Update parse error"+str(ex))
