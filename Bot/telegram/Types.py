
class ChatUser:
    def __init__(self, id, first_name, last_name, username):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


class User(ChatUser):
    def __init__(self, id, is_bot, first_name, last_name, username, language_code):
        super().__init__(id, first_name, last_name, username)
        self.is_bot = is_bot
        self.language_code = language_code


class ChatPhoto:
    def __init__(self, small_file_id, big_file_id):
        self.small_file_id = small_file_id
        self.big_file_id = big_file_id


class Chat(ChatUser):
    def __init__(self, id, type, title, username,
                 first_name, last_name, all_members_are_administrators, photo,
                 description, invite_link, pinned_message, sticker_set_name, can_set_sticker_set
                 ):
        super().__init__(id, first_name, last_name, username)
        self.type = type
        self.title = title
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = ChatPhoto(photo['small_file_id'],
                               photo['big_file_id']) if photo is not None else None
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = create_message(pinned_message)
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set


class MessageEntity:
    def __init__(self, type, offset, length, url, user):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = create_user(user)


class PhotoSize:
    def __init__(self, file_id, width, height, file_size):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size


class Invoice:
    def __init__(self, title, description, start_parameter, currency, total_amount):
        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount


class SuccessfulPayment:
    def __init__(self, currency, total_amount, invoice_payload,
                 shipping_option_id, order_info, telegram_payment_charge_id,
                 provider_payment_charge_id
                 ):
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = create_order_info(order_info)
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id


class OrderInfo:
    def __init__(self, name, phone_number, email, shipping_address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = create_shipping_address(shipping_address)


class ShippingAddress:
    def __init__(self, country_code, state, city, street_line1, street_line2, post_code):
        self.country_code = country_code
        self.city = city
        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.post_code = post_code


class Message:
    def __init__(self, message_id, user, date, chat, forward_from, forward_from_chat,
                 forward_from_message_id, forward_signature, forward_date, reply_to_message,
                 edit_date, author_signature, text, entities, caption_entities,
                 audio, document, game, photo, sticker, video, voice, video_note,
                 caption, contact, location, venue, new_chat_members, left_chat_member,
                 new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created,
                 supergroup_chat_created, channel_chat_created, migrate_to_chat_id,
                 migrate_from_chat_id, pinned_message, invoice, successful_payment
                 ):
        self.message_id = message_id
        self.user = create_user(user)
        self.date = date
        self.chat = create_chat(chat)
        self.forward_from = create_user(forward_from)
        self.forward_from_chat = create_chat(forward_from_chat)
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_date = forward_date
        self.reply_to_message = create_message(reply_to_message)
        self.edit_date = edit_date
        self.author_signature = author_signature
        self.text = text
        self.entities = create_message_entity(entities)
        self.caption_entities = caption_entities
        self.audio = audio
        self.document = document
        self.game = game
        self.photo = create_photo_size(photo)
        self.sticker = sticker
        self.video = video
        self.voice = voice
        self.video_note = video_note
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.new_chat_members = [create_user(u) for u in new_chat_members] if new_chat_members is not None else None
        self.left_chat_member = create_user(left_chat_member)
        self.new_chat_title = new_chat_title
        self.new_chat_photo = create_photo_size(new_chat_photo)
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = create_message(pinned_message)
        self.invoice = invoice
        self.successful_payment = SuccessfulPayment(successful_payment['currency'],
                                                    successful_payment['total_amount'],
                                                    successful_payment['invoice_payload'],
                                                    successful_payment.get('shipping_option_id', None),
                                                    successful_payment.get('order_info', None),
                                                    successful_payment['telegram_payment_charge_id'],
                                                    successful_payment['provider_payment_charge_id']
                                                    ) if successful_payment is not None else None

class Location:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class Inline:
    def __init__(self, user, location, query):
        self.user = create_user(user)
        self.location = Location(location['longitude'],
                                 location['latitude']
                                 ) if location is not None else None
        self.query = query

class InlineQuery(Inline):
    def __init__(self, id, user, location, query, offset):
        super().__init__(user, location, query)
        self.id = id
        self.offset = offset

class ChosenInlineResult(Inline):
    def __init__(self, result_id, user, location, inline_message_id, query):
        super().__init__(user, location, query)
        self.result_id = result_id
        self.inline_message_id = inline_message_id

class CallbackQuery:
    def __init__(self, id, user, message, inline_message_id, chat_instance, data, game_short_name):
        self.id = id
        self.user = create_user(user)
        self.message = create_message(message)
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.data = data
        self.game_short_name = game_short_name

class ShippingQuery:
    def __init__(self, id, user, invoice_payload, shipping_address):
        self.id = id
        self.user = create_user(user)
        self.invoice_payload = invoice_payload
        self.shipping_address = create_shipping_address(shipping_address)

class PreCheckoutQuery:
    def __init__(self, id, user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
        self.id = id
        self.user = create_user(user)
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = create_order_info(order_info)


class Update:
    def __init__(self, update_id, message, edited_message, channel_post,
                 edited_channel_post, inline_query, chosen_inline_result,
                 callback_query, shipping_query, pre_checkout_query):
        self.update_id = update_id
        self.message = create_message(message)
        self.edited_message = create_message(message)
        self.channel_post = create_message(channel_post)
        self.edited_channel_post = create_message(edited_channel_post)
        self.inline_query = InlineQuery(
            inline_query['id'],
            inline_query['from'],
            inline_query.get('location', None),
            inline_query['query'],
            inline_query['offset']
        ) if inline_query is not None else None

        self.chosen_inline_result = ChosenInlineResult(
            chosen_inline_result['result_id'],
            chosen_inline_result['from'],
            chosen_inline_result.get('location', None),
            chosen_inline_result.get('inline_message_id', None),
            chosen_inline_result['query']
        ) if chosen_inline_result is not None else None

        self.callback_query = CallbackQuery(
            callback_query['id'],
            callback_query['from'],
            callback_query.get('message', None),
            callback_query.get('inline_message_id', None),
            callback_query.get['chat_instance'],
            callback_query.get('data', None),
            callback_query.get('game_short_name', None)
        ) if callback_query is not None else None

        self.shipping_query = ShippingQuery(
            shipping_query['id'],
            shipping_query['from'],
            shipping_query['invoice_payload'],
            shipping_query['shipping_address']
        ) if shipping_query is not None else None

        self.pre_checkout_query = PreCheckoutQuery(
            pre_checkout_query['id'],
            pre_checkout_query.get('from', None),
            pre_checkout_query['currency'],
            pre_checkout_query['total_amount'],
            pre_checkout_query['invoice_payload'],
            pre_checkout_query.get('shipping_option_id', None),
            pre_checkout_query.get('order_info', None)
        ) if pre_checkout_query is not None else None



def create_message(field):
    return Message(
            field['message_id'],
            field.get('from', None),
            field['date'],
            field['chat'],
            field.get('forward_from', None),
            field.get('forward_from_chat', None),
            field.get('forward_from_message_id', None),
            field.get('forward_signature', None),
            field.get('forward_date', None),
            field.get('reply_to_message', None),
            field.get('edit_date', None),
            field.get('author_signature', None),
            field.get('text', None),
            field.get('entities', None),
            field.get('caption_entities', None),
            field.get('audio', None),
            field.get('document', None),
            field.get('game', None),
            field.get('photo', None),
            field.get('sticker', None),
            field.get('video', None),
            field.get('voice', None),
            field.get('video_note', None),
            field.get('caption', None),
            field.get('contact', None),
            field.get('location', None),
            field.get('venue', None),
            field.get('new_chat_members', None),
            field.get('left_chat_member', None),
            field.get('new_chat_title', None),
            field.get('new_chat_photo', None),
            field.get('delete_chat_photo', None),
            field.get('group_chat_created', None),
            field.get('supergroup_chat_created', None),
            field.get('channel_chat_created', None),
            field.get('migrate_to_chat_id', None),
            field.get('migrate_from_chat_id', None),
            field.get(' field', None),
            field.get('invoice', None),
            field.get('successful_payment', None),
            ) if field is not None else None

def create_chat(field):
    return Chat(
                field['id'], field['type'], field.get('title', None),
                field.get('username', None), field.get('first_name', None),
                field.get('last_name', None),
                field.get('all_members_are_administrators', None),
                field.get('photo', None), field.get('description', None),
                field.get('invite_link', None), field.get('pinned_message', None),
                field.get('sticker', None), field.get('can_set_sticker_set', None)
                ) if field is not None else None

def create_user(field):
    return User(field['id'], field.get('is_bot', None),
                     field['first_name'],
                     field.get('last_name', None),
                     field.get('fieldname', None),
                     field.get('language_code', None)
                     ) if field is not None else None


def create_message_entity(field):
    return [MessageEntity(
        m['type'],
        m['offset'],
        m['length'],
        m.get('url', None),
        m.get('user', None)
    ) for m in field] if field is not None else None

def create_photo_size(field):
    return [
        PhotoSize(
            p['file_id'],
            p['width'],
            p['height'],
            p['file_size']
        )
        for p in field
    ] if field is not None else None

def create_shipping_address(field):
    return ShippingAddress(field['country_code'],
                                            field['state'],
                                            field['city'],
                                            field['street_line1'],
                                            field['street_line2'],
                                            field['post_code']
                                            ) if field is not None else None

def create_order_info(field):
    return OrderInfo(field['name'],
                                field['phone_number'],
                                field['email'],
                                field['shipping_address']
                               ) if field is not None else None
