import asyncio
from userbot.events import register
from userbot import CMD_HELP


@register(pattern=r".sca (.*)", outgoing=True)
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    input_str = event.pattern_match.group(1)
    action = "typing"
    if input_str:
        action = input_str
    async with borg.action(event.chat_id, action):
        await asyncio.sleep(120)  # type for 120 seconds
        
        
CMD_HELP.update({
    "sca": ".sca typing, contact, game, location, vooce, round, video, photo, document, cancel\
    \nUsage: Creating Fake Chat actions Just for fun."
})