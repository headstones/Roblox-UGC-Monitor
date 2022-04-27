import requests
import json
import time
import discord
from discord import Webhook, RequestsWebhookAdapter
################################################################################################
discordWebhook = "https://discord.com/api/webhooks... webhook stuff" # ONLY THING U NEED TO EDIT 
################################################################################################
################# DONT TOUCH ANYTHING BELOW THIS UNLESS U HAVE A WORKING BRAIN #################
API = "https://catalog.roblox.com/v1/search/items?category=CommunityCreations&limit=10&sortType=3&subcategory=CommunityCreations"
infourl = "https://api.roblox.com/marketplace/productinfo?assetId="
webhook = Webhook.from_url(discordWebhook, adapter=RequestsWebhookAdapter())
olddata = requests.get(API).json()
print("Scanning the roblox catalog..")
while True: # a shitty while true loop because i am a noob
    time.sleep(5)
    newdata = requests.get(API).json()
    if newdata != olddata:
        print("Catalog update detected!")
        olddata = newdata
        itemid = newdata["data"][0]["id"]
        iteminfo = requests.get(infourl + str(itemid)).json()
        createddate = iteminfo["Created"]
        updatedate = iteminfo["Updated"]
        if createddate[0:12] == updatedate[0:12]: #compares upload and update dates to see if it was updated in the past hour
            print(f"{itemid} is new, uploaded at {createddate}, updated at {updatedate}")
            # webhook stuff
            itemname = iteminfo["Name"]
            itemprice = iteminfo["PriceInRobux"]
            thumbnail = f"https://www.roblox.com/asset-thumbnail/image?assetId={itemid}&width=420&height=420&format=png"
            itemlink = "https://www.roblox.com/catalog/" + str(itemid)
            Embed = discord.Embed(title="UGC Accessory Uploaded.", description=f"https://www.roblox.com/catalog/{itemid}", color=0x00ff00)
            Embed.add_field(name="Item Name", value=itemname, inline=True)
            Embed.add_field(name="Item Price", value=itemprice, inline=True)
            Embed.set_thumbnail(url=thumbnail)
            webhook.send(embed=Embed)
        else: #nofity that it was only updated
            print(f"{itemid} was updated, uploaded at {createddate}, updated at {updatedate}")
            itemname = iteminfo["Name"]
            itemprice = iteminfo["PriceInRobux"]
            thumbnail = f"https://www.roblox.com/asset-thumbnail/image?assetId={itemid}&width=420&height=420&format=png"
            itemlink = "https://www.roblox.com/catalog/" + str(itemid)
            Embed = discord.Embed(title="UGC Accessory Updated.", description=f"https://www.roblox.com/catalog/{itemid}", color=0x00ff00)
            Embed.add_field(name="Item Name", value=itemname, inline=True)
            Embed.add_field(name="Item Price", value=itemprice, inline=True)
            Embed.set_thumbnail(url=thumbnail)
            webhook.send(embed=Embed)
    else:
        continue
# if something breaks keep the window open
input("Press enter to exit")
