#GITHUB File Uploader Plugin for userbot. Heroku Automation should be Enabled. Else u r not that lazy // For lazy people
#Instructions:- Set GITHUB_ACCESS_TOKEN and GIT_REPO_NAME Variables in Heroku vars First
#usage:- .commit reply_to_any_plugin //can be any type of file too. but for plugin must be in .py 
#By:- @Zero_cool7870


from github import Github
import aiohttp
import asyncio
import os
import time
from datetime import datetime
from telethon.tl.types import DocumentAttributeVideo
from userbot.modules.download import humanbytes, progress, time_formatter
from userbot.events import register
from userbot import GITHUB_ACCESS_TOKEN, GIT_REPO_NAME


GIT_TEMP_DIR = "./temp/"

@register(outgoing=True, pattern="^.commit(?: |$)(.*)")
async def download(gomitgo):
	if gomitgo.fwd_from:
		return	
	if GITHUB_ACCESS_TOKEN is None:
		await gomitgo.edit("`Please ADD Proper Access Token from github.com`") 
		return   
	if GIT_REPO_NAME is None:
		await gomitgo.edit("`Please ADD Proper Github Repo Name of your userbot`")
		return 
        await gomitgo.reply("Processing ...")
	input_str = gomitgo.pattern_match.group(1)
	if not os.path.isdir(GIT_TEMP_DIR):
		os.makedirs(GIT_TEMP_DIR)
	start = datetime.now()
	reply_message = await gomitgo.get_reply_message()
	try:
		c_time = time.time()
		downloaded_file_name = await gomitgo.client.download_media(
			reply_message,
			GIT_TEMP_DIR,
			progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
			progress(d, t, gomitgo, c_time, "trying to download")
			)
		)
	except Exception as e: 
		await gomitgo.edit(str(e))
	else:
		end = datetime.now()
		duration = (end - start).seconds
		await gomitgo.delete()
		await gomitgo.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, duration))
		await gomitgo.edit("Committing to Github....")
		await git_commit(downloaded_file_name,mone)

async def git_commit(file_name,mone):        
	content_list = []
	access_token = GITHUB_ACCESS_TOKEN
	g = Github(access_token)
	file = open(file_name,"r",encoding='utf-8')
	commit_data = file.read()
	repo = g.get_repo(GIT_REPO_NAME)
	print(repo.name)
	create_file = True
	contents = repo.get_contents("")
	for content_file in contents:
		content_list.append(str(content_file))
		print(content_file)
	for i in content_list:
		create_file = True
		if i == 'ContentFile(path="'+file_name+'")':
			return await gomitgo.edit("`File Already Exists`")
			create_file = False
	file_name = "userbot/modules/"+file_name		
	if create_file == True:
		file_name = file_name.replace("./temp/","")
		print(file_name)
		try:
			repo.create_file(file_name, "Uploaded New Module", commit_data, branch="master")
			print("Committed File")
			await gomotgo.edit("`Committed on Your Github Repo.`")
		except:
			print("Cannot Create Plugin")
			await gomitgo.edit("Cannot Upload Plugin")
	else:
		return await gomitgo.edit("`Committed Suicide`")
