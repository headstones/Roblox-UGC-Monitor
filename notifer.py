import requests
import json
import time
import discord
from discord import Webhook, RequestsWebhookAdapter
# the holy grail of  variables
discordWebhook = "https://discord.com/api/webhooks... webhook stuff" # ONLY ONE U NEED TO CHANGE 
####### dont touch anything below this unless you are the owner of a working brain 
API = "https://catalog.roblox.com/v1/search/items?category=CommunityCreations&limit=10&sortType=3&subcategory=CommunityCreations"
infourl = "https://api.roblox.com/marketplace/productinfo?assetId="
webhook = Webhook.from_url(discordWebhook, adapter=RequestsWebhookAdapter())
olddata = requests.get(API).json()
print("Scanning for new items..")
# if somethign breaks/errors just ignore it
while True:
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
            olddata = newdata
            # webhook stuff
            itemname = iteminfo["Name"]
            itemprice = iteminfo["PriceInRobux"]
            thumbnail = f"https://www.roblox.com/asset-thumbnail/image?assetId={itemid}&width=420&height=420&format=png"
            itemlink = "https://www.roblox.com/catalog/" + str(itemid)
            Embed = discord.Embed(title="New UGC accessory detected!", description=f"https://www.roblox.com/catalog/{itemid}", color=0x00ff00)
            Embed.add_field(name="Item Name", value=itemname, inline=True)
            Embed.add_field(name="Item Price", value=itemprice, inline=True)
            Embed.set_thumbnail(url=thumbnail)
            webhook.send(embed=Embed)
        else:
            print(f"{itemid} created at {createddate}, updated at {updatedate} is not new :(")
    else:
        print("No updates detected")
        continue
# if something breaks keep the window open
input("Press enter to exit")
