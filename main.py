import requests, re, os, time, discord, requests, datetime, asyncio
from discord.ext import commands
from discord import app_commands
from bs4 import BeautifulSoup
from keep_alive import *
from functions.micron import *
from functions.corsair import *
from functions.gskill import *
from functions.all import *


class aclient(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.default())
    self.synced = False

  async def on_ready(self):

    print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)


def micron(code):
  partnum = code
  code = str(decode(code))
  embed = discord.Embed(
    title=f"{partnum.upper()}",
    url=
    f"https://www.micron.com/support/tools-and-utilities/fbga?fbga={partnum}",
    description=f"{code}",
    color=0xadd8e6)
  embed.set_thumbnail(
    url=
    f"https://upload.wikimedia.org/wikipedia/de/thumb/0/03/Micron_Logo.svg/1200px-Micron_Logo.svg.png"
  )
  try:
    embed.add_field(name=f"Rev {code.split(':')[1]}",
                    value=f"{version(code)}",
                    inline=True)
  except:
    pass
  try:
    embed.add_field(name=f"{density(code)} Bits", value=f"⠀", inline=True)
  except:
    pass
  try:
    embed.set_footer(text="_exa")
  except:
    pass
  embed.timestamp = datetime.datetime.utcnow()

  return embed


def corsair(code):
  partnum = (clean(code))

  corsairvers = f"v{partnum[:1]}.{partnum[1:]}"
  embed = discord.Embed(title=corsairvers, description="⠀", color=0xc08080)
  embed.set_thumbnail(url=f"{image(manu(partnum))}")
  embed.add_field(name=f"{manu(partnum)}",
                  value=f"{dens(partnum)} Gbit",
                  inline=True)
  embed.add_field(name=f"{rev(partnum)}-Die", value="⠀", inline=True)
  #if check(partnum) is not None:
  #embed.add_field(name=f"Note", value=f"{check(partnum)}", inline=False)
  embed.set_footer(text="_exa")
  embed.timestamp = datetime.datetime.utcnow()

  return embed


def gskill(code):
  o42 = code.upper()
  gskillvers = o42[-5:]
  embed = discord.Embed(title=gskillvers,
                        description=f"{ddr(o42)}",
                        color=0xc08080)
  embed.set_thumbnail(url=f"{image(gskill_manuf(o42))}")
  embed.add_field(name=f"{gskill_manuf(o42)}",
                  value=f"{die_density(o42)} Gbit",
                  inline=True)
  embed.add_field(name=f"{die_revision(o42)}-Die",
                  value=f"{GK_die_organisation(o42)}",
                  inline=True)
  embed.set_footer(text="_exa")
  embed.timestamp = datetime.datetime.utcnow()

  return embed


def sort(code):
  try:
    partnum = (clean(code))
    if len(partnum) == 3:
      return corsair(code)
    if len(partnum) == 1:
      return micron(code)
    else:
      return gskill(code)
  except:
    print("Error please double check format")
    pass

#use 'c9blm' as the Code to test, it should return a micron logo in top right of embed
@tree.command(
  name='code',
  description=
  'Gets Die information from some memory sticks. Limited to Crucial, Corsair, and G.Skill currently.'
)
@discord.app_commands.describe(code='Version Code on label or package')
async def slash2(interaction: discord.Interaction, code: str):
  if len(code) < 12:
    try:
      await interaction.response.send_message(embed=sort(code), ephemeral=True)
    except:
      print(sort(code))
  else:
    await interaction.response.send_message(
      f"Error, please double check formatting.", ephemeral=True)


@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
  print(interaction.user.id)
  #change the ID to your own
  if interaction.user.id == 447432884286914561:
    await tree.sync()
    await interaction.response.send_message('Success- Branch Synced')
  else:
    await interaction.response.send_message(
      'You must be the owner to use this command!', ephemeral=True)


@tree.command(name='latency', description='Converts a timing from nCK to ')
@discord.app_commands.describe(
  frequency='Effective speed in Mbps or Mt/s',
  timing='Timing in nCK (how you find it in the BIOS)')
async def slash2(interaction: discord.Interaction, frequency: int,
                 timing: int):
  latency = timing * 2000 / frequency
  await interaction.response.send_message(
    f"The latency is {round(latency, 2)}ns", ephemeral=True)


keep_alive()
client.run(os.environ['DISCORD_BOT_SECRET'])
