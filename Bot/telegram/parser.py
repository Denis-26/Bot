from .Types import Update


def parser(update):
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
