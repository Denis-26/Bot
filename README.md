# Quick start 

### Install 

* install pip3
```bash
sudo python3-pip install
```
* install library
```bash
git clone https://github.com/Denis-26/Bot.git
cd ./Bot
sudo pip3 install .
```

### Example of simple echo bot

```python
import asyncio
from Bot import telegram

config = {
    "token": "BotToken",
    "web_hook": "https://domain_name.ex:443",              # new updates will come here with post request
    "bot_url": "https://domain_name.ex",     
    "port": "443"
}

class MyCoolBot(telegram.Bot):
    def __init__(self, config, loop=None):
        super().__init__(config, loop=loop)

    async def handler(self, update):                       # this method must be redefined, all updates will come here 
        user_id = update.message.user.id                   # get id of user, who sent message
        text = update.message.text                         # get text which was send by user
        await self.api.send_message(user_id, text)         # send user's text back

async def main(bot, loop):
    await bot.run()
    await bot.api.delete_webhook()
    await bot.api.set_webhook(config['web_hook'])


if __name__ == "__main__":
    new_loop = asyncio.get_event_loop()
    bot = MyCoolBot(config, loop=new_loop)
    new_loop.create_task(main(bot, new_loop))
    try:
        new_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        bot.stop_running()
        new_loop.close()
```

------------------

## Documentation
When you inherit from **telegram.Bot**, your class get field **self.api**. This field has type **_Api**.
Also your class will get next methods:

```python
Bot(config, loop=None)
coroutine run(self)
stop_running()
coroutine handler(self, update) # must be redefined
```

### Methods of **_Api** class

```python
coroutine set_webhook(self, web_hook, cert=None)
coroutine delete_webhook(self, chat_id, text, **kwargs)
coroutine send_message(self, chat_id, text, **kwargs)
coroutine answer_inline_query(self, answer_inline_query)
coroutine answer_inline_query(self, answer_inline_query)
coroutine send_sticker(self, chat_id, sticker, **kwargs)
coroutine send_photo(self, chat_id, photo, **kwargs)
coroutine send_photo(self, chat_id, photo, **kwargs)
coroutine send_invoice(self, chat_id, title, payload, provider_token, start_parameter, currency, prices, **kwargs)
coroutine answer_precheckout_query(self, pre_checkout_query_id, **kwargs)
coroutine get_file(self, file_id)
coroutine delete_message(self, chat_id, m_id)
```

### Tools (Buttons)

telegram has some tools for work with buttons

#### telegram.ReplyKeyboardMarkup() 
methods: 
```python
add_button("button_text")
add_par() # create \n in buttons markup
```


#### telegram.InlineKeyboardMarkup() 
methods: 
```python
add_button("button_text", callback_data=some_data)
add_par() # create \n in buttons markup
```

