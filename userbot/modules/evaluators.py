# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

""" Userbot module for executing code and terminal commands from Telegram. """

import asyncio
import time
import io
from getpass import getuser
from os import remove
from sys import executable
import subprocess
from telethon import events, sync, errors, functions, types
import inspect
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
from userbot.events import register
from userbot import MAX_MESSAGE_SIZE_LIMIT


@register(outgoing=True, pattern="^.eval(?: |$)(.*)")
async def evaluate(query):
    """ For .eval command, evaluates the given Python expression. """
    if not query.text[0].isalpha() and query.text[0] not in ("/", "#", "@", "!"):
        if queri.fwd_from:
            return
        await queri.edit("Processing ...")
        cmd = queri.pattern_match.group(1)
        reply_to_id = queri.message.id
        if queri.reply_to_msg_id:
            reply_to_id = query.reply_to_msg_id
        evaluation = eval(cmd)
        await query.delete()
        # https://t.me/telethonofftopic/43873
        try:
            if inspect.isawaitable(evaluation):
                evaluation = await evaluation
        except (Exception) as e:
            evaluation = str(e)

        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, f"Eval query {evaluation} was executed successfully"
            )


@register(outgoing=True, pattern=r"^.exec(?: |$)([\s\S]*)")
async def run(run_q):
    """ For .exec command, which executes the dynamically created program """
    if not run_q.text[0].isalpha() and run_q.text[0] not in ("/", "#", "@", "!"):
        if run_q.fwd_from:
            return
        DELAY_BETWEEN_EDITS = 0.3
        PROCESS_RUN_TIME = 100
        cmd = run_q.pattern_match.group(1)
        reply_to_id = run_q.message.id
        if run_q.reply_to_msg_id:
            reply_to_id = run_q.reply_to_msg_id
        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**Output:**\n"
        stdout, stderr = await process.communicate()
        if len(stdout) > MAX_MESSAGE_SIZE_LIMIT:
            with io.BytesIO(str.encode(stdout)) as out_file:
                out_file.name = "exec.text"
                await run_q.client.send_file(
                    run_q.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=OUTPUT,
                    reply_to=reply_to_id
                )
                await run_q.delete()
        if stderr.decode():
            await run_q.edit(f"{OUTPUT}`{stderr.decode()}`")
            return
        await run_q.edit(f"{OUTPUT}`{stdout.decode()}`")

        if BOTLOG:
            await run_q.client.send_message(
                BOTLOG_CHATID,
                "Exec query " + OUTPUT + " was executed successfully"
            )


@register(outgoing=True, pattern="^.term(?: |$)(.*)")
async def terminal_runner(term):
    """ For .term command, runs bash commands and scripts on your server. """
    if not term.text[0].isalpha() and term.text[0] not in ("/", "#", "@", "!"):
        curruser = getuser()
        command = term.pattern_match.group(1)
        try:
            from os import geteuid
            uid = geteuid()
        except ImportError:
            uid = "This ain't it chief!"

        if term.is_channel and not term.is_group:
            await term.edit("`Term commands aren't permitted on channels!`")
            return

        if not command:
            await term.edit("``` Give a command or use .help term for \
                an example.```")
            return

        if command in ("userbot.session", "config.env"):
            await term.edit("`That's a dangerous operation! Not Permitted!`")
            return

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if len(result) > 4096:
            output = open("output.txt", "w+")
            output.write(result)
            output.close()
            await term.client.send_file(
                term.chat_id,
                "output.txt",
                reply_to=term.id,
                caption="`Output too large, sending as file`",
            )
            remove("output.txt")
            return

        if uid is 0:
            await term.edit(
                "`"
                f"{curruser}:~# {command}"
                f"\n{result}"
                "`"
            )
        else:
            await term.edit(
                "`"
                f"{curruser}:~$ {command}"
                f"\n{result}"
                "`"
            )

        if BOTLOG:
            await term.client.send_message(
                BOTLOG_CHATID,
                "Terminal Command " + command + " was executed sucessfully",
            )

CMD_HELP.update({
    "eval": ".eval 2 + 3\nUsage: Evalute mini-expressions."
})
CMD_HELP.update({
    "exec": ".exec print('hello')\nUsage: Execute small python scripts."
})
CMD_HELP.update({
    "term": ".term ls\nUsage: Run bash commands and scripts on your server."
})
