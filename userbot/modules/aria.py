#This Lit Module By:- @Zero_cool7870 Sar

  
import aria2p
import asyncio
import os
from userbot.events import register


cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"

aria2_is_running = os.system(cmd)

aria2 = aria2p.API(
		aria2p.Client(
			host="http://localhost",
			port=6800,
			secret=""
		)
	)


@register(outgoing=True, pattern="^.magnet(?: |$)(.*)")
async def magnet_download(maggu):
	if maggu.fwd_from:
		return   
	var = maggu.text
	var = var[8:]
	
	magnet_uri = var
	magnet_uri = magnet_uri.replace("`","")
	print(magnet_uri)

	#Add Magnet URI Into Queue
	try:
		download = aria2.add_magnet(magnet_uri)
	except:
		await maggu.edit("`Error: Make Sure Magnet link is correct.`")	
		return

	await maggu.edit("`Downloading From Magnet Link: `\n\n"+magnet_uri+"\nType show to check status")
	await asyncio.sleep(5)
	await maggu.delete()		

@register(outgoing=True, pattern="^.tor(?: |$)(.*)")
async def torrent_download(thor):
	if thor.fwd_from:
		return

	var = thor.text[5:]
	
	torrent_file_path = var	
	torrent_file_path = torrent_file_path.replace("`","")
	print(torrent_file_path)

	#Add Torrent Into Queue
	try:
		download = aria2.add_torrent(torrent_file_path, uris=None, options=None, position=None)
	except:
		await thor.edit("`Torrent File Not Found...`")
		return

	gid = download.gid
	complete = None
	while complete != True:
		file = aria2.get_download(gid)
		complete = file.is_complete
		try:
			msg = "Downloading File: "+str(file.name) +"\nSpeed: "+ str(file.download_speed_string())+"\n"+"Progress: "+str(file.progress_string())+"\nStatus: "+str(file.status)+"\nETA:  "+str(file.eta_string())+"\n\n"
			await thor.edit(msg)
			await asyncio.sleep(10)
		except Exception as e:
			#print(str(e))
			pass	

	await thor.edit("File Downloaded Successfully:\n`"+download.name+"`")

@register(outgoing=True, pattern="^.url(?: |$)(.*)")
async def magnet_download(uri):
	if uri.fwd_from:
		return
	var = uri.text[5:]
	print(var)	
	uris = [var]

	#Add URL Into Queue 
	try:	
		download = aria2.add_uris(uris, options=None, position=None)
	except Exception as e:
		await uri.edit("`Error:\n`"+str(e))
		return

	gid = download.gid
	complete = None
	while complete != True:
		file = aria2.get_download(gid)
		complete = file.is_complete
		try:
			msg = "Downloading File: "+str(file.name) +"\nSpeed: "+ str(file.download_speed_string())+"\n"+"Progress: "+str(file.progress_string())+"\nStatus: "+str(file.status)+"\nETA:  "+str(file.eta_string())+"\n\n"	
			await uri.edit(msg)
			await asyncio.sleep(10)
		except Exception as e:
			#print(str(e))
			pass	
			
	await uri.edit("File Downloaded Successfully:\n`"+file.name+"`")



@register(outgoing=True, pattern="^.ariaRM(?: |$)(.*)")
async def remove_all(ironman):
	if ironman.fwd_from:
		return
	try:
		removed = aria2.remove_all(force=True)	
		aria2.purge_all()
	except:
		pass
			
	if removed == False:  #If API returns False Try to Remove Through System Call.
		os.system("aria2p remove-all")

	await ironman.edit("`Removed All Downloads.`")  

@register(outgoing=True, pattern="^.ariaP(?: |$)(.*)")
async def pause_all(poo):
	if poo.fwd_from:
		return
	paused = aria2.pause_all(force=True)	#Pause ALL Currently Running Downloads.

	await poo.edit("Output: "+str(paused))

@register(outgoing=True, pattern="^.ariaResume(?: |$)(.*)")
async def resume_all(room):
	if room.fwd_from:
		return

	resumed = aria2.resume_all()

	await room.edit("Output: "+str(resumed))	

@register(outgoing=True, pattern="^.show(?: |$)(.*)")
async def show_all(saw):
	if saw.fwd_from:
		return
	output = "output.txt"
	#Show All Downloads
	downloads = aria2.get_downloads() 

	msg = ""

	for download in downloads:
		msg = msg+"File: "+str(download.name) +"\nSpeed: "+ str(download.download_speed_string())+"\n"+"Progress: "+str(download.progress_string())+"\nStatus: "+str(download.status)+"\nETA:  "+str(download.eta_string())+"\n\n"
	print(msg)
	if len(msg) <= 4096:
		await saw.edit("`Current Downloads: `\n"+msg)
	else:
		await saw.edit("`Output is huge. Sending as a file...`")
		with open(output,'w') as f:
			f.write(msg)
		await asyncio.sleep(2)	
		await saw.delete()	
		await saw.client.send_file(
			saw.chat_id,
			output,
			force_document=True,
            supports_streaming=False,
            allow_cache=False,
			reply_to=saw.message.id,
			)
