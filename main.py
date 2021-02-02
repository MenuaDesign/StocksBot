import discord
import requests
import json
import time

client = discord.Client()
string1 = 'https://finnhub.io/api/v1/search?q='
string2 = '&token=c07jt7748v6retjahm00'
TEST = requests.get('https://finnhub.io/api/v1/quote?symbol=NIO&token=c07jt7748v6retjahm00')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_ready():
    print("Logged {0.user}\nReady".format(client))
typed = 0
ids = 1
myEmbed = discord.Embed(color=0x00ff00)


async def itemloader(message,dict):
    global ids
    global myEmbed
    print(dict)
    if ids > len(dict):
        await message.channel.send("```No results [type an ID, to show results] | [type 'STOP' to stop]```")
        return
    for j in range(5):
        myEmbed = discord.Embed(color=0x00ff00)
        myEmbed.set_author(name=str(ids))
        print(dict)
        myEmbed.add_field(name="Description: ", value=dict[ids - 1]['description'], inline=False)
        myEmbed.add_field(name="Symbol: ", value=dict[ids - 1]['symbol'], inline=False)
        ids += 1
        await message.channel.send(embed=myEmbed)
        if ids > len(dict):
            break
    await message.channel.send("```Choose a ID [type an ID, to show results] | [type 'MORE' for more results] | [type 'STOP' to stop]```")

Auther = None
list = []
count = 0
messageamount = 0

@client.event
async def on_message(stock):
    global Auther
    global messageamount
    global list
    if messageamount == 0:
        messageamount +=1
        Auther = stock.author
    if stock.author == Auther:
        try:
            ss =""
            icon ="$"
            global typed
            global r
            global myEmbed
            global ids
            if stock.author == client.user:
                return
            if typed == 0:
                if stock.content[0] == icon:
                    for i in stock.content:
                        if i != icon:
                            ss += i
                    print("Loading",end="")
                    a = 0
                    for i in range(0,11):
                        time.sleep(0.5)
                        a =a+1
                        print(".",end="")
                        if a ==4:
                            a = 0
                            print("",end="\b"*4)
                    tmp = string1 + ss.upper() + string2
                    r = requests.get(tmp)
                    print("",end="\r")

                    string3 = 'https://finnhub.io/api/v1/quote?symbol='
                    string4 = '&token=c07jt7748v6retjahm00'
                    for i in range(len(r.json()['result'])):
                        b = r.json()['result'][i]['symbol']
                        bb = requests.get(string3 + b.upper() + string4)
                        if 'error' not in bb.json():
                            list.append(r.json()['result'][i])

                    print("Count: " + str(r.json()['count']))
                    myEmbed = discord.Embed(color=0x00ff00)
                    myEmbed.set_author(name="Count: " + str(len(list)))
                    await stock.channel.send(embed=myEmbed)
                    await itemloader(stock, list)
                    typed +=1
                    return
            elif typed == 1:
                if stock.content.lower() == "more":
                    await itemloader(stock, list)
                    return
                if stock.content.lower() == "stop":
                    await stock.channel.send("```See you next time!```")
                    typed = 0
                    ids = 1
                    messageamount = 0
                    list = []
                    return
                print(stock.content)
                print(len(list))
                if int(stock.content) >= 1 and int(stock.content) <= len(list):
                    myEmbed = discord.Embed(color=0x00ff00)
                    myEmbed.set_author(name=list[(int(stock.content)-1)]['symbol'])
                    string3 = 'https://finnhub.io/api/v1/quote?symbol='
                    string4 = '&token=c07jt7748v6retjahm00'
                    b = list[(int(stock.content)-1)]['symbol']
                    print(b)
                    bb = requests.get(string3 + b.upper() +string4)
                    print(bb.json())
                    if 'error' in bb.json():
                        await stock.channel.send("```You don't have acces to this resource, please try again!```")
                        return
                    myEmbed.add_field(name="Current: ", value=bb.json()['c'], inline=False)
                    myEmbed.add_field(name="Highest: ", value=bb.json()['h'], inline=False)
                    myEmbed.add_field(name="Lowest: ", value=bb.json()['l'], inline=False)
                    await stock.channel.send(embed=myEmbed)
                    ids = 1
                    typed =0
                    messageamount = 0
                    list=[]
                    return
                await stock.channel.send("```Wrong ID!, Try again [type an ID, to show results] | [type 'MORE' for more results] | [type 'STOP' to stop]```")
            else:
                typed = 0
        except ValueError:
            await stock.channel.send("```Invalid, please try again!```")
client.run('ODAzMzYzMzEyNDIyMzU0OTk0.YA8sYw.EkR2WJr0IPLV65H-Ncfo1RTXWME')

