from telethon import events
from telethon.utils import pack_bot_file_id
from sql_helpers.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome
from userbot.events import register


@register(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await event.client.delete_messages(  # pylint:disable=E0602
                        event.chat_id,
                        cws.previous_welcome
                )
                a_user = await event.get_user()
                current_saved_welcome_message = cws.custom_welcome_message
                mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
                current_message = await event.reply(
                    current_saved_welcome_message.format(mention=mention),
                    file=cws.media_file_id
                )
                update_previous_welcome(event.chat_id, current_message.id)


@register(pattern=r".savewelcome (.*)", outgoing=True)
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        bot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, True, 0, bot_api_file_id)
        await event.edit("Welcome note saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], True, 0)
        await event.edit("Welcome note saved. ")


@register(pattern=r".clearwelcome (.*)", outgoing=True)
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit(
        "Welcome note cleared. " + \
        "The previous welcome message was `{}`.".format(cws.custom_welcome_message)
    )
