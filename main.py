# bot.py
import os
import random
import webserver
from webserver import keep_alive
import asyncio
import requests
import discord
from discord.ext import commands
from discord.utils import get
import time
import datetime

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = False
intents.presences = False

client = discord.Client(intents=intents)
iWaroz = 'me'

def botcolor(guild):
  color = getmember(guild, 716189086653874229).color
  return color

def getrole(guild, role):
    for i in guild.roles:
        if str(i) == role:
            return i

def getroleid(guild, role):
    for i in guild.roles:
        if i.id == role:
            return i

def getmember(guild, id):
    for i in guild.members:
        if i.id == id:
            return i

def fn(num):
    num = str(num)
    lo = len(num) % 3
    numl = []
    if lo > 0:
        numl = [num[:lo]]
    num = num[lo:]
    while len(num) > 0:
        numl.append(num[:3])
        num = num[3:]
    return ','.join(numl).replace('N,o D,ata', "No Data")

async def activityrefresh():
  while True:
    members = 0
    channels = 0
    for i in client.guilds:
      members += len(i.members)
    uniques = fn(len(client.users))
    activity = discord.Activity(name=f'p?help | v1.3 | p?updates', type=discord.ActivityType.playing) # | {fn(len(client.guilds))} servers | {fn(members)} total members | {uniques} unique users
    await client.change_presence(activity=activity)
    await asyncio.sleep(10)

bot_id = 716189086653874229

cache = []
world = {}
continents = {}
states = {}
regions = []

async def update_cache():
  global cache
  global world
  global continents
  global states
  global regions
  while True:
    regions = []
    cache = requests.get('https://disease.sh/v2/countries').json()
    states = requests.get('https://disease.sh/v2/states').json()
    continents = requests.get('https://disease.sh/v2/continents').json()
    world = requests.get('https://disease.sh/v2/all').json()
    for i in states:
      regions.append(i["state"])
    for i in continents:
      regions.append(i["continent"])
    for i in cache:
      regions.append(i["country"])
    await asyncio.sleep(600)

import aiohttp

bot = client.user

dbltoken = os.getenv("TOPGG_TOKEN")
url = "https://discordbots.org/api/bots/" + str(bot_id) + "/stats"
headers = {"Authorization" : dbltoken}

@client.event
async def on_guild_leave(server):
  payload = {"server_count"  : len(client.guilds)}
  async with aiohttp.ClientSession() as aioclient:
    await aioclient.post(url, data=payload, headers=headers)

@client.event
async def on_guild_join(server):
  payload = {"server_count"  : len(client.guilds)}
  async with aiohttp.ClientSession() as aioclient:
    await aioclient.post(url, data=payload, headers=headers)

data = []

@client.event
async def on_ready():
  print('Bot ready')
  #await client.get_user(247741991310327810).send('Hi. Sent by iWaroz. The other bot was deleted by discord but I can get the new version to dm you.')
  activity = discord.Activity(name='COVID-19', type=discord.ActivityType.watching)
  #await client.change_presence(activity=activity)
  global iWaroz
  iWaroz = client.get_user(296356465273470998)
  client.loop.create_task(activityrefresh())
  client.loop.create_task(update_cache())
  payload = {"server_count"  : len(client.guilds)}
  async with aiohttp.ClientSession() as aioclient:
    await aioclient.post(url, data=payload, headers=headers)

@client.event
async def on_message(message):
  g = message.guild
  if message.author.bot: return
  prefix = 'p?'
  if message.author.id == 715902532110516304 and message.content.startswith('p?say '):
    await message.channel.send(message.content[6:])
    return
  if message.content in ['<@!716189086653874229>', '<@716189086653874229>']:
    try:
      await message.author.send('Hi! Here are some basic commands:\n\n**p?stats <country|continent|us-state>** to get some up-to-date data.\n**p?top <stat>** to get the top 10 countries in a certain stat, dp **p?top** for a list of possible stats.\n**p?help** for an overrall list.\n**p?updates** for the most recent bot updates.\n**p?info** for our support server.\n\n```diff\n- If the bot is not working, use p?diagnose and I will find issues.```\nJoin our support server, it is within the Neon server: https://discord.gg/dY3abHG')
      try:
        await message.channel.send(f'Sent you a dm {message.author.mention}!')
      except: pass
    except:
      await message.channel.send('Hi! Here are some basic commands:\n\n**p?stats <country|continent|us-state>** to get some up-to-date data.\n**p?top <stat>** to get the top 10 countries in a certain stat, dp **p?top** for a list of possible stats.\n**p?help** for an overrall list.\n**p?updates** for the most recent bot updates.\n**p?info** for our support server.\n\n```diff\n- If the bot is not working, use p?diagnose and I will find issues.```\nJoin our support server, it is within the Neon server: https://discord.gg/dY3abHG')
  if len(message.content) > len(prefix):
    if message.content[:len(prefix)].lower() == prefix:
      cmd = message.content[len(prefix):]
      cmd = cmd.split(' ')
      sendembeds = message.channel.permissions_for(getmember(g, bot_id)).embed_links
      if cmd[0] in ['stats', 'top', 'help', 'info']:
        if not message.channel.permissions_for(getmember(g, bot_id)).send_messages:
          await message.author.send(f'I do not have the `Send Messages` permission in <#{message.channel.id}> channel. Please use a different channel or ask a server administrator to enable my permissions in there.')
        elif not message.channel.permissions_for(getmember(g, bot_id)).embed_links:
          pass
          #await message.channel.send('I do not have the `Send Embedded Links` permission. Please enable this permission if possible, or contact a server administrator. I will use a plaint')
      if cmd[0] == 'stats':
        cmd[1] = " ".join(cmd[1:])
        if cmd[1] == '': cmd[1] = 'world'
        if not sendembeds:
          text = "I do not have the `Send Embedded Links` permission, please enable this for better readability.\n\n"
        try: country = cmd[1]
        except: country = 'world'
        if country == 'world':
          data = world
          if not sendembeds:
            text += '**World Statistics**\n\n'
          else:
            embed = discord.Embed(title='World Statistics', color=botcolor(g), timestamp=datetime.datetime.fromtimestamp(data["updated"]/1000))
        else:
          for i in cache:
            if i["country"].lower() == cmd[1].lower():
              data = i
          usecountry = True
          try: data['updated']
          except: usecountry = False
          if not usecountry:
            usecontinent = True
            for i in continents:
              if i["continent"].lower() == cmd[1].lower():
                data = i
                i.update({'country':i["continent"]})
            try: data['updated']
            except:
              usecontinent = False
            if not usecontinent:
              for i in states:
                if i["state"].lower() == cmd[1].lower():
                  data = i
                  i.update({'country':i["state"]})
              try: data['updated']
              except:
                await message.channel.send('Invalid country, continent or us state.')
                return
          if not sendembeds:
            text += f'**{data["country"]} Statistics**\n\n'
          else:
            embed = discord.Embed(title=f'{data["country"]} Statistics', color=botcolor(g), timestamp=datetime.datetime.fromtimestamp(data["updated"]/1000))
        for i in ["recovered", "critical"]:
          if not i in data:
            data.update({i:"No Data"})
        if not sendembeds:
          text += f'**Total Statistics**\nTotal Cases: `{fn(data["cases"])}`\nTotal Deaths: `{fn(data["deaths"])}`\nRecovered Cases: `{fn(data["recovered"])}`\nRecorded Tests: `{fn(data["tests"])}`\n\n**Current Statistics**\nActive Cases: `{fn(data["active"])}`\nCritical Cases: `{fn(data["critical"])}`\n\n**Today\'s Statistics**\nNew Cases: `{fn(data["todayCases"])}`\nNew Deaths: `{fn(data["todayDeaths"])}`'
          await message.channel.send(text)
          return
        if False: pass
        else:
          embed.add_field(name='Total Statistics', value=f'Total Cases: `{fn(data["cases"])}`\nTotal Deaths: `{fn(data["deaths"])}`\nRecovered Cases: `{fn(data["recovered"])}`\nRecorded Tests: `{fn(data["tests"])}`')
          embed.add_field(name='Current Statistics', value=f'Active Cases: `{fn(data["active"])}`\nCritical Cases: `{fn(data["critical"])}`', inline=False)
          embed.add_field(name="Today's Statistics", value=f'New Cases: `{fn(data["todayCases"])}`\nNew Deaths: `{fn(data["todayDeaths"])}`')
          embed.set_footer(text='Information Updated')
          await message.channel.send('', embed=embed)
      elif cmd[0] == 'dblowner' and message.author.id == 715902532110516304:
        await message.channel.send('The owner of this bot is `iWaroz#6869`.')
      elif cmd[0] == 'top':
        try: stat = cmd[1]
        except: stat = ''
        try: tops = cmd[2]
        except: tops = 10
        if not stat in ['deaths', 'cases', 'active', 'recovered', 'newcases', 'newdeaths', 'caseproportion']:
          await message.channel.send('Invalid Statistic! Please use one of the following: `deaths`, `cases`, `active`, `recovered`, `newcases`, `newdeaths` and `caseproportion`.')
          return
        else:
          data = cache
        lookupstat = {'deaths':'deaths','cases':'cases','recovered':'recovered','newcases':'todayCases','newdeaths':'todayDeaths','caseproportion':'activePerOneMillion'}[stat]
        nicename = {'deaths':'Deaths','cases':'Cases','recovered':'Recovered Cases','newcases':'New Cases Today','newdeaths':'New Deaths Today','caseproportion':'Infected Proportion'}[stat]
        countries = []
        for i in data:
          countries.append([i[lookupstat], i['country']])
        countries.sort()
        countries.reverse()
        msg = ''
        for x in range(int(tops)):
          value = countries[x][0]
          if stat == 'caseproportion':
            value = str(round(value / 10000, 3)) + '%'
          else:
            value = fn(value)
          msg += f'#{x+1}. {countries[x][1]} with `{value}` {nicename}\n'
        if sendembeds:
          embed = discord.Embed(title=f'Top Covid-19 {nicename}', description=msg, color=botcolor(g), timestamp=datetime.datetime.fromtimestamp(data[0]["updated"]/1000))
          embed.set_footer(text='Information Updated')
          await message.channel.send('', embed=embed)
        else:
          await message.channel.send(f'I do not have the `Send Embedded Links` permission, please enable this for better readability.\n\n**Top Covid-19 {nicename}**\n\n{msg}')
      elif cmd[0] == 'help':
        if sendembeds:
          embed = discord.Embed(title='Bot Commands', description='To use the Pandemic bot, you can use the following commands:', color=botcolor(g))
          embed.add_field(name='**p?stats (country)**', value='Check covid-19 statistics about said country. Leaving this field blank or using "world" will give global stats')
          embed.add_field(name='**p?top <stats> (amount)**', value='Check which countries have the highest of certain statistics such as `deaths`, `cases`, `active`, `recovered`, `newcases`, `newdeaths` and `caseproportion`. Leaving the amount field blank will default to 10 and it cannot be higher than 20.', inline=False)
          embed.add_field(name='**p?info**', value='Learn more about Nova Labs and the api used which allows this bot to be used.', inline=False)
          await message.channel.send('', embed=embed)
        else:
          await message.channel.send('I do not have the `Send Embedded Links` permission, please enable this for better readability.\n\n**Bot Commands**\n\nTo use the Pandemic bot, you can use the following commands:\n\n**p?stats (country)**\nCheck covid-19 statistics about said country. Leaving this field blank or using "world" will give global stats\n\n**p?top <stats> (amount)**\nCheck which countries have the highest of certain statistics such as `deaths`, `cases`, `active`, `recovered`, `newcases`, `newdeaths` and `caseproportion`. Leaving the amount field blank will default to 10 and it cannot be higher than 20.\n\n**p?info**\nLearn more about Nova Labs and the api used which allows this bot to be used.')
      elif cmd[0] == 'info':
        if sendembeds:
          embed = discord.Embed(title='Bot Information', description='Here is some information about the Pandemic bot', color=botcolor(g))
          embed.add_field(name='**Neon Labs**', value='The Pandemic bot was created by neon labs, owned by <@715902532110516304>. We also have other bots you should check out!\nTwitter: https://twitter.com/neonbot\nSupport Server: https://discord.gg/dY3abHG')
          embed.add_field(name='**Our API**', value="The Pandemic bot takes it's data from the NovelCovid API (https://disease.sh/). Thanks to them for making this bot possible!", inline=False)
          await message.channel.send('', embed=embed)
        else:
          await message.channel.send('I do not have the `Send Embedded Links` permission, please enable this for better readability.\n\n**Bot Information**\n\nHere is some information about the Pandemic bot\n\n**Neon Labs**\nThe Pandemic bot was created by neon labs, owned by iWaroz#6869. We also have other bots you should check out!\nTwitter: https://twitter.com/neonbot\nSupport Server: https://discord.gg/dY3abH\n\n**Our API**\nThe Pandemic bot takes it\'s data from the NovelCovid API (https://disease.sh/). Thanks to them for making this bot possible!')
      elif cmd[0] == 'diagnose':
        await message.channel.send(f'Check your dms, {message.author.mention}!')
        noread = []
        nosend = []
        noembed = []
        slowmode = []
        for i in g.channels:
          if not i.permissions_for(g.me).read_messages:
            noread.append(i.mention)
          if not i.permissions_for(g.me).send_messages:
            nosend.append(i.mention)
          if not i.permissions_for(g.me).embed_links:
            noembed.append(i.mention)
          if not i.permissions_for(g.me).manage_messages and i.slowmode_delay > 0:
            slowmode.append(i.mention)
        text = ''
        if len(noread) > 0:
          text += f'I cannot read messages in the {", ".join(noread)} channel(s) and thus cannot respond to commands in there. Please enable the `Read Messages` permission for me in those channels.\n'
        if len(nosend) > 0:
          text += f'I cannot send messages in the {", ".join(nosend)} channel(s) and thus cannot respond to commands in there. Please enable the `Send Messages` permission for me in those channels.\n'
        if len(noembed) > 0:
          text += f'I cannot embed links in the {", ".join(noembed)} channel(s). My responses will not look nice so please enable the `Embed Links` permission for me in those channels.\n'
        if len(slowmode) > 0:
          text += f'I have detected slowmode in the following channels in which I cannot bypass: {", ".join(slowmode)}. If you wish me to be able to bypass this restriction, please give me the `Manage Messages` permission in these channels.\n'
        if text == '': text = 'No problems found. Rerun this command at any point for another check.\n'
        text += '\nMake sure to join our support server if you have any other issues. (Pandemic support is included within the Neon server)\nhttps://discord.gg/dY3abHG'
        try:
          await message.author.send(text)
        except:
          await message.channel.send(text)
      elif cmd[0] == 'updates':
        if not sendembeds:
          await message.channel.send('I need the `Embed Links` permission to use this command. You can join our support server for more info: discord.gg/dY3abHG')
        else:
          embed = discord.Embed(title='Latest Updates', description='Join our support server to be the first to see new updates: https://discord.gg/dY3abHG', color=botcolor(g))
          embed.add_field(name='v1.1', value='- If the bot does not have chat perms, someone using a command will be sent a message warning them about the lack of permissions.\n- If the bot cannot send embedded links, it will instead post it in purely text form.\n- The p?botstats command now shows the largest 10 servers it is in, if you are on this list and do not want to appear, dm iWaroz#6869 about it.\n- Improved response speed by 20 times.', inline=False)
          embed.add_field(name='v1.2', value='- Added compatibility for locations with spaces in them.\n- Added continents to p?stats.\n- Added US states to p?stats.\n- Added p?updates to look at the latest updates.', inline=False)
          embed.add_field(name='v1.3', value='- Added p?diagnose to find potential issues in the server.\n- Pinging the bot will now dm you some commands and help.', inline=False)
          await message.channel.send('', embed=embed)

@client.event
async def on_guild_join(guild):
  await client.get_guild(700607174497271829).get_channel(724506869493923851).send('', embed=discord.Embed(description=f'I joined the server {guild} with id {guild.id} and {len(guild.members)} members.', color=0x8dff73))

@client.event
async def on_guild_remove(guild):
  await client.get_guild(700607174497271829).get_channel(724506869493923851).send('', embed=discord.Embed(description=f'I left the server {guild} with id {guild.id} and {len(guild.members)} members.', color=0xff7373))

keep_alive()
client.run(token)