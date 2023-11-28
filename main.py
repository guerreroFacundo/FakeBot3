# Bot para probar cosas randoms
import os
import typing
import discord
from discord import Embed
import random
from discord.ext import commands
from discord import app_commands
from flask.cli import main
import xmltodict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import keep_alive, dolarPrecios , IA
import asyncio
import subprocess
import flask
from flask import request, Flask, render_template
os.system('pip install pymongo[srv]')
import json, requests
subprocess.call(['pip', 'install', 'pymongo[srv]'])


app = Flask(__name__)
app.config["DEBUG"] = True
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
#client = discord.Client(intents=intents)
MY_GUILDS = []




class MyClient(discord.Client):
  
    
  def __init__(self, *, intents: discord.Intents):
      print("Iniciando bot...")
      super().__init__(intents=intents)
      self.tree = app_commands.CommandTree(self)
  
  # In this basic example, we just synchronize the app commands to one guild.
  # Instead of specifying a guild to every command, we copy over our global commands instead.
  # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
  async def setup_hook(self):
      
      print(f"Syncing commands to {len(self.guilds)} guilds...")
      # This copies the global commands over to your guild.
      #for guild in MY_GUILDS:
      # print(f"Syncing commands for {guild.name} ({guild.id})")
      await self.tree.fetch_commands()
      await self.tree.sync()

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print('Loggeado como: {0.user}'.format(client))
    
    for guild in client.guilds:
      print(guild.id)
      MY_GUILDS.append(guild.id)
      


@client.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
async def generate(interaction: discord.Interaction,message:str):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(IA.IAimple.generate(message))

@client.tree.command()
async def generatefact(interaction: discord.Interaction,message:str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(IA.IAimple.generateFact(message))

@client.tree.command()
async def dolar(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True)
  result = dolarPrecios.findUsd.obtenerDolar()
  await interaction.followup.send(result)






##EVENTOS CON EL PREFIX EN #
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    ##ESTO TE DEVUELVE LOS VALORES DE LOS DOLARES
    if message.content.startswith('#dolar'):
      result = dolarPrecios.findUsd.obtenerDolar()
      await message.channel.send(result)

    ##ESTE ES EL GENERATE FUN FACT PARA QUE TE GENERE UN DATO SOBRE LO QUE LE MANDES
    if message.content.startswith('#generateFact'):
        strmsj =str(message.content[13:])
        responseTexto=IA.IAimple.generateFact(strmsj)
        await message.channel.send(responseTexto)

    ##ESTE ES EL GENERATE PARA QUE GENERE CUALQUIER COSA QUE LE MANDES LUEGO DEL COMANDO
    if message.content.startswith('#generate'):
      strmsj =str(message.content[9:])
      responseTexto=IA.IAimple.generate(strmsj)
      await message.channel.send(responseTexto)







      
keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))
app.run()



