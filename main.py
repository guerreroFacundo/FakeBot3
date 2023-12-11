# Bot para probar cosas randoms
import os
import discord
from discord import app_commands
import dolarPrecios, IA
import asyncio
from datetime import datetime
from pytz import timezone
from flask import Flask
import youtube
import R6
import Steam, imagenes
from discord.ui import Button, View
from flask_app import app, run, keep_alive
import json

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
    if not self.synced:  #check if slash commands have been synced
      await tree.sync(
      )  #guild specific: leave blank if global (global registration can take 1-24 hours)
      self.synced = True
    print(f"We have logged in as {self.user}.")
    # Llamar al método para guardar comandos al estar listo
    comandosguardados.guardarComandos()


#Llamo a la clase para sincronizar los comandos
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)


class comandosguardados:

  def guardarComandos():
    comandos = tree.get_commands()
    comand_data = {}
    for comando in comandos:
      comand_data[comando.name] = str(comando.description)
    with open('comandos.json', 'w') as json_file:
      json.dump(comand_data, json_file, indent=4)
    print("termine de guardar los comandos")


#----------------------------------------------INICIO Comandos "/" ---------------------------------------------------
@tree.command(name="say", description="El bot dice lo que quieras")
async def say(interaction: discord.Interaction, msg: str):
  await interaction.response.send_message(msg, tts=True, ephemeral=True)


@tree.command(name="generate",
              description="El bot va a generar lo que le pidas por texto")
async def generate(interaction: discord.Interaction, message: str):
  await interaction.response.defer(thinking=True)
  sinlaletrafea = message.replace("ñ", "U+00F1")
  await interaction.followup.send(embed=IA.IAimple.generate(sinlaletrafea))


@tree.command(name="generate_image",
              description="El bot va a generar lo que le pidas con replicate")
async def generate_image(interaction: discord.Interaction, message: str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(embed=IA.IAimple.generateImage(message))


@tree.command(name="generate_image_op",
              description="El bot va a generar lo que le pidas con Dalle")
async def generate_image_openai(interaction: discord.Interaction,
                                message: str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(embed=IA.IAimple.generateImageOpenai(message))


@tree.command(
    name="generate_fact",
    description="El bot va a generar un dato divertido de lo ingresado")
async def generatefact(interaction: discord.Interaction, message: str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(embed=IA.IAimple.generateFact(message))

@tree.command(name="dolar",
  description="El bot te dice el precio del dolar en tiempo real")
async def dolar(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True)
  result = dolarPrecios.findUsd.obtenerDolar2()
  await interaction.followup.send(embed=result)

@tree.command(name="steam",
              description="El bot te transforma el dolar ingresado a pesos")
async def steam(interaction: discord.Interaction, message: str):
  await interaction.response.defer(thinking=True)
  await interaction.followup.send(dolarPrecios.findUsd.steam(message))


@tree.command(
    name="join",
    description="El bot te une al canal de voz en el que te encuentras")
async def join(interaction: discord.Interaction):
  if (interaction.user.voice):
    await interaction.user.voice.channel.connect()
    await interaction.response.send_message("Conectado UwU")
  else:
    await interaction.response.send_message(
        "No estas conectado en el canal de voz papu. ewe")


@tree.command(name="leave",
              description="El bot se desconecta del canal de voz")
async def leave(interaction: discord.Interaction):
  if (interaction.client.voice_clients):
    await interaction.guild.voice_client.disconnect(force=True)
    await interaction.response.send_message("Me voy papu.")
  else:
    await interaction.response.send_message(
        "No estoy conectado en el canal de voz pa")


@tree.command(name="play", description="El bot reproducira lo que le pidas")
async def play(interaction: discord.Interaction, url: str):
  await interaction.response.send_message(f'Voy a reproducir : {url}')
  await youtube.music.play(interaction, url)


@tree.command(
    name="r6_stats",
    description="El bot te dice las estadisticas de tu perfil de Rainbow 6")
async def rainbow_stats(interaction: discord.Interaction, player_name: str):
  resultado = await R6.rainbow.get_stats(player_name)

  async def next_call(interaction):
    if len(resultado) > 1:
      button3 = Button(label="Back", style=discord.ButtonStyle.gray)
      button3.callback = back_call
      view3 = View()
      view3.add_item(button3)
      await interaction.response.edit_message(embed=resultado[1], view=view3)

  async def back_call(interaction):
    if len(resultado) > 1:
      button2 = Button(label="Next", style=discord.ButtonStyle.gray)
      button2.callback = next_call
      view2 = View()
      view2.add_item(button2)
      await interaction.response.edit_message(embed=resultado[0], view=view2)

  button = Button(label="Next", style=discord.ButtonStyle.gray)
  button.callback = next_call
  view = View()
  if len(resultado) > 1:
    view.add_item(button)
  await interaction.response.send_message(embed=resultado[0], view=view)


@tree.command(name="steam_profile",
              description="El bot te dice la informacion de tu perfil de steam"
              )
async def steam_profile(interaction: discord.Interaction, player_name: str):
  await interaction.response.defer(thinking=True)
  resultado = Steam.steam.serch_player(player_name)
  await interaction.followup.send(embed=resultado)


@tree.command(name="bonk", description="Hace que golpees a alguien :v")
async def bonk(interaction: discord.Interaction, member: discord.Member):
  await interaction.response.defer(thinking=True)
  await imagenes.imagenes.armarImagenBonk2(interaction, member)
  await interaction.followup.send(file=discord.File("imagenes/perfil_completo.png"))


@tree.command(name="stop",
              description="El bot detiene la reproduccion de musica")
async def stop(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True)
  await youtube.music.stop(interaction)
  await interaction.followup.send("Se detuvo la musica UwU ")


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
    strmsj = str(message.content[13:])
    responseTexto = IA.IAimple.generateFact(strmsj)
    await message.channel.send(responseTexto)

  ##ESTE ES EL GENERATE PARA QUE GENERE CUALQUIER COSA QUE LE MANDES LUEGO DEL COMANDO
  if message.content.startswith('#generate'):
    strmsj = str(message.content[9:])
    responseTexto = IA.IAimple.generate(strmsj)
    await message.channel.send(responseTexto)


#----------------------------------------------Keep alive y run-----------------------------------------------

keep_alive()
client.run(os.getenv('TOKEN'))
app.run()
