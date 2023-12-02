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
from datetime import datetime
from pytz import timezone   
import subprocess
from discord import opus
from discord.ext import tasks
import flask
from flask import request, Flask, render_template
#os.system('pip install pymongo[srv]')
import json, requests
import yt_dlp as youtube_dl
import youtube
#subprocess.call(['pip', 'install', 'pymongo[srv]'])


app = Flask(__name__)
app.config["DEBUG"] = True
intents = discord.Intents.all()
intents.message_content = True
intents.members = True


#Clase para sincronizar los comandos a todos los servidores
class MyClient(discord.Client):
  
    
  def __init__(self, *, intents: discord.Intents):
      print("Iniciando bot...")
      super().__init__(intents=intents)
      self.synced = False 
  async def on_ready(self):
      print("Bot conectado")
      # await tomen_awita_version_vicky.start()
      # await schedule_daily_message.start()
      await self.wait_until_ready()
      if not self.synced: #check if slash commands have been synced 
        await tree.sync() #guild specific: leave blank if global (global registration can take 1-24 hours)
        self.synced = True
      print(f"We have logged in as {self.user}.")
            
#Llamo a la clase para sincronizar los comandos
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
      

#----------------------------------------------INICIO Comandos "/" ---------------------------------------------------
@tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@tree.command()
async def generate(interaction: discord.Interaction,message:str):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(IA.IAimple.generate(message))

@tree.command()
async def generate_image(interaction: discord.Interaction,message:str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(IA.IAimple.generateImage(message))

@tree.command()
async def generatefact(interaction: discord.Interaction,message:str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(IA.IAimple.generateFact(message))

@tree.command()
async def dolar(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True)
  result = dolarPrecios.findUsd.obtenerDolar()
  await interaction.followup.send(result)

@tree.command()
async def steam(interaction: discord.Interaction,message:str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(dolarPrecios.findUsd.steam(message))

@tree.command()
async def join(interaction: discord.Interaction):
  if(interaction.user.voice):
    await interaction.user.voice.channel.connect()
    await interaction.response.send_message("Conectado UwU")
  else:
    await interaction.response.send_message("No estas conectado en el canal de voz papu. ewe")
    
@tree.command()
async def leave(interaction: discord.Interaction):
  if(interaction.client.voice_clients):
    await interaction.guild.voice_client.disconnect(force=True)
    await interaction.response.send_message("Me voy papu.")
  else:
    await interaction.response.send_message("No estoy conectado en el canal de voz pa")

@tree.command()
async def play(interaction: discord.Interaction,url:str):
  await interaction.response.send_message(f'Voy a reproducir : {url}')
  await youtube.music.play(interaction,url)
  
    
# @tasks.loop(hours=1,minutes=30,seconds=0)
# async def tomen_awita_version_vicky():
#   argentina = timezone('America/Argentina/Buenos_Aires')
#   sa_time = datetime.now(argentina)
#   print("Loop.Hora :",sa_time.hour)
#   if(sa_time.hour >= 9 and sa_time.hour<=21):
#     allowed_mentions = discord.AllowedMentions(everyone = True)
#     channel_to_upload_to =client.get_channel(int(os.getenv('CHANEL')))
#     #channel_to_upload_to =client.get_channel(982486319727018045)
#     print("Channel obtenido: ",channel_to_upload_to)
#     vickyid =os.getenv('VICKYID')
#     listado=[]
#     file=open("vickyjson.json")
#     data = json.load(file)
#     for frase in data['frases']:
#       listado.append(frase)
#     print("JSON: ",data)
#     print("JSON keys: ",data.keys())
#     randomchoice=random.choice(listado)
#     print("Frase aleatoria: ",randomchoice['frase'])
#     formatedFrase =randomchoice['frase']
#     await channel_to_upload_to.send(content = (f'Tomen agua UwU, <@{vickyid}> {formatedFrase}'), allowed_mentions = allowed_mentions)
  

@tree.command()
async def stop(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True)
  await youtube.music.stop(interaction)
  await interaction.followup.send("Se detuvo la musica UwU ")


# @tasks.loop(hours=1,minutes=30.0,seconds=0)
# async def schedule_daily_message():
#   argentina = timezone('America/Argentina/Buenos_Aires')
#   sa_time = datetime.now(argentina)
#   print("Loop.Hora :",sa_time.hour)
#   if(sa_time.hour >= 9 and sa_time.hour<=21):
#     allowed_mentions = discord.AllowedMentions(everyone = True)
#     channel_to_upload_to =client.get_channel(1071229379239215115)
#     await channel_to_upload_to.send(content = "Tomen agua UwU", allowed_mentions = allowed_mentions)
    
    

#----------------------------------------------FIN Comandos "/" -----------------------------------------------------

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







#----------------------------------------------Keep alive y run-----------------------------------------------

keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))
app.run()



