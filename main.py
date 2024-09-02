# Bot para probar cosas randoms
import json
import os
import re

import aiohttp
import discord
from discord import app_commands
from discord.ui import Button, View
from dotenv import load_dotenv
from flask import Flask

import Geminni
import OpenIA
import R6
import Steam
import dolarPrecios
import imagenes
import weather
from PaginationView import PaginationView
from flask_app import keep_alive

load_dotenv()
app = Flask(__name__)
app.config["DEBUG"] = True
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

# Crear un embed para mostrar la información
embedError = discord.Embed(title='Error', color=0xff0000)
message_history = {}
MAX_HISTORY = int(os.getenv("MAX_HISTORY"))


# Clase para sincronizar los comandos a todos los servidores
class MyClient(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        print("Iniciando bot...")
        super().__init__(intents=intents)
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print("Bot conectado")
        # await tomen_awita_version_vicky.start()
        # await schedule_daily_message.start()
        await self.wait_until_ready()
        if not self.synced:  # Chequeamos que el /comando se haya sincronizado
            # Limpiar comandos globales
            global_commands = await self.tree.fetch_commands()
            # Sincronizar los comandos nuevos
            for guild in self.guilds:
                self.tree.copy_global_to(guild=guild)
            await self.tree.sync()
            self.synced = True
            # Obtener los comandos globales
            global_commands = await self.tree.fetch_commands()
            print(f"Comandos sincronizados: {global_commands}")
        # Llamar al método para guardar comandos al estar listo
        comandosguardados.guardarComandos(self.tree)
        print(f"Nos hemos iniciado como: {self.user}.")


class comandosguardados:
    def guardarComandos(tree: app_commands.CommandTree):
        print("Inicio guardar comandos.")
        comandos = tree.get_commands()
        comand_data = {}
        for comando in comandos:
            comand_data[comando.name] = str(comando.description)
        with open('comandos.json', 'w') as json_file:
            json.dump(comand_data, json_file, indent=4)
        print("FIN guardar comandos.")


# Llamo a la clase para sincronizar los comandos
client = MyClient(intents=intents)


# ----------------------------------------------INICIO Comandos "/" ---------------------------------------------------
@client.tree.command(name="help", description="Muestra todos los comandos que tiene el bot disponible")
async def help(interaction: discord.Interaction):
    try:
        # Obtener todos los comandos desde el árbol de comandos
        comandos = client.tree.get_commands()

        # Crear un embed para mostrar los comandos
        embed = discord.Embed(title="Comandos Disponibles", color=discord.Color.blue())

        for comando in comandos:
            embed.add_field(name=f"/{comando.name}", value=comando.description, inline=False)

        # Enviar el embed como respuesta
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="say", description="El bot dice lo que quieras")
async def say(interaction: discord.Interaction, msg: str):
    try:
        await interaction.response.send_message(msg, tts=True, ephemeral=True)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="dolar",
                     description="El bot te dice el precio del dolar en tiempo real")
async def dolar(interaction: discord.Interaction):
    result = discord.Embed(title='Error', color=0x00ff00)
    await interaction.response.defer(thinking=True)
    try:
        result = await dolarPrecios.findUsd.obtenerDolar4()
        await interaction.followup.send(embed=result)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="steam",
                     description="El bot te transforma el dolar ingresado a pesos")
async def steam(interaction: discord.Interaction, dolares: str):
    try:
        await interaction.response.defer(thinking=True)
        respuesta = await dolarPrecios.findUsd.steam(dolares)
        await interaction.followup.send(embed=respuesta)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="clima",
                     description="El bot te dice el clima")
async def clima(interaction: discord.Interaction, ciudad: str):
    try:
        await interaction.response.defer(thinking=True)
        responseObtenerClima = await weather.clima.obtenerClima(ciudad)
        await interaction.followup.send(embed=responseObtenerClima)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="climafuturo", description="El bot te dice el clima dentro de los próximos 14 días")
async def climaFuture(interaction: discord.Interaction, ciudad: str):
    try:
        responseObtenerClimaFuture = await weather.clima.obtenerClimaFuture(ciudad)  # Esto devuelve una lista de embeds

        pagination_view = PaginationView(responseObtenerClimaFuture)
        initial_embed = responseObtenerClimaFuture[0]
        # Envía el mensaje inicial y asigna el mensaje a self.message
        await interaction.response.send_message(embed=initial_embed, view=pagination_view)
        pagination_view.message = await interaction.original_response()  # Asigna la respuesta original a self.message

    except Exception as e:
        embedError = discord.Embed(title="Error", description=f"Se generó un ERROR: {e}", color=discord.Color.red())
        await interaction.followup.send(embed=embedError)

@client.tree.command(name="chatgpt",
                     description="Mensajes a chatGPT")
async def chatgpt(interaction: discord.Interaction, mensaje: str):
    try:
        await interaction.response.defer(thinking=True)
        respuestaChatGPT = await OpenIA.chatGPT.mandarPrompt(mensaje=mensaje)
        await interaction.followup.send(embed=respuestaChatGPT)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="gemini",
                     description="Mensajes a gemini")
async def chatgpt(interaction: discord.Interaction, mensaje: str):
    try:
        await interaction.response.defer(thinking=True)
        respuesta = await Geminni.geminni.mandarPrompt(mensaje=mensaje)
        await interaction.followup.send(embed=respuesta)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


# On Message Function
@client.event
async def on_message(message):
    if message.author == client.user or message.mention_everyone:
        return
    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        cleaned_text = clean_discord_message(message.content)

        async with message.channel.typing():
            if message.attachments:
                print("Nuevo mensaje con imagen de:" + str(message.author.id) + ": " + cleaned_text)
                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(ext) for ext in
                           ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        await message.add_reaction('🎨')

                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    await message.channel.send('No pudimos descargar esta imagen.')
                                    return
                                image_data = await resp.read()
                                response_text = await Geminni.geminni.generate_response_with_image_and_text(image_data,
                                                                                                            cleaned_text)
                                await split_and_send_messages(message, response_text,
                                                              1700)  # Esto es porque a discord le molesta los mensajes largos
                                return
            else:
                print("Nuevo mensaje de:" + str(message.author.id) + ": " + cleaned_text)
                if "RESET" in cleaned_text:  # Si tiene la palabra reset entonces se reinicia el historial
                    if message.author.id in message_history:
                        del message_history[message.author.id]
                    await message.channel.send("🤖 Se reseteo el historial para el usuario: " + str(message.author.name))
                    return
                await message.add_reaction('💬')
                if (MAX_HISTORY == 0):
                    response_text = await Geminni.geminni.generate_response_with_text(cleaned_text)
                    await split_and_send_messages(message, response_text, 1700)
                    return;
                update_message_history(message.author.id, cleaned_text)
                response_text = await Geminni.geminni.generate_response_with_text(
                    get_formatted_message_history(message.author.id))
                update_message_history(message.author.id, response_text)
                await split_and_send_messages(message, response_text, 1700)


# ---------------------------------------------Message History-------------------------------------------------
def update_message_history(user_id, text):
    if user_id in message_history:
        message_history[user_id].append(text)
        if len(message_history[user_id]) > MAX_HISTORY:
            message_history[user_id].pop(0)
    else:
        message_history[user_id] = [text]


def get_formatted_message_history(user_id):
    if user_id in message_history:
        return '\n\n'.join(message_history[user_id])
    else:
        return "No hay mensajes disponibles para este usuario."


# ---------------------------------------------Sending Messages-------------------------------------------------
async def split_and_send_messages(message_system, text, max_length):
    messages = []
    for i in range(0, len(text), max_length):
        sub_message = text[i:i + max_length]
        messages.append(sub_message)
    for string in messages:
        await message_system.channel.send(string)


def clean_discord_message(input_string):
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

# ----------------------------------------------------------------------------------------------------------------
@client.tree.command(
    name="r6_stats",
    description="El bot te dice las estadisticas de tu perfil de Rainbow 6")
async def rainbow_stats(interaction: discord.Interaction, player_name: str):
    try:
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
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="steam_profile",
                     description="El bot te dice la informacion de tu perfil de steam"
                     )
async def steam_profile(interaction: discord.Interaction, player_name: str):
    await interaction.response.defer(thinking=True)
    try:
        resultado = Steam.steam.serch_player(player_name)
        await interaction.followup.send(embed=resultado)
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


@client.tree.command(name="bonk", description="Hace que golpees a alguien :v")
async def bonk(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(thinking=True)
    try:
        await imagenes.imagenes.armarImagenBonk2(interaction, member)
        await interaction.followup.send(file=discord.File(
            "F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/perfil_completo.png"))
    except Exception as e:
        print(f"Se genero un ERROR: {e}")
        embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
        await interaction.followup.send(embed=embedError)


# @client.tree.command(
#     name="join",
#     description="El bot te une al canal de voz en el que te encuentras")
# async def join(interaction: discord.Interaction):
#     if (interaction.user.voice):
#         try:
#             await interaction.user.voice.channel.connect()
#             await interaction.response.send_message("Conectado UwU")
#         except Exception as e:
#             print(f"Se genero un ERROR: {e}")
#             embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
#             await interaction.followup.send(embed=embedError)
#     else:
#         await interaction.response.send_message(
#             "No estas conectado en el canal de voz papu. ewe")


# @client.tree.command(name="leave",
#                      description="El bot se desconecta del canal de voz")
# async def leave(interaction: discord.Interaction):
#     if (interaction.client.voice_clients):
#         try:
#             await interaction.guild.voice_client.disconnect(force=True)
#             await interaction.response.send_message("Me voy papu.")
#         except Exception as e:
#             print(f"Se genero un ERROR: {e}")
#             embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
#             await interaction.followup.send(embed=embedError)
#     else:
#         await interaction.response.send_message(
#             "No estoy conectado en el canal de voz pa")


# @client.tree.command(name="play", description="El bot reproducira lo que le pidas")
# async def play(interaction: discord.Interaction, url: str):
#     await interaction.response.send_message(f'Voy a reproducir : {url}')
#     try:
#         await youtube.music.play(interaction, url)
#     except Exception as e:
#         print(f"Se genero un ERROR: {e}")
#         embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
#         await interaction.response.send_message(embed=embedError)


# @client.tree.command(name="stop",
#                      description="El bot detiene la reproduccion de musica")
# async def stop(interaction: discord.Interaction):
#     await interaction.response.defer(thinking=True)
#     try:
#         await youtube.music.stop(interaction)
#         await interaction.followup.send("Se detuvo la musica UwU ")
#     except Exception as e:
#         print(f"Se genero un ERROR: {e}")
#         embedError.add_field(name='Mensaje Error', value=f'{e}', inline=False)
#         await interaction.followup.send(embed=embedError)


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

# ----------------------------------------------FIN Comandos "/" -----------------------------------------------------

# ----------------------------------------------Keep alive y run-----------------------------------------------

keep_alive()
client.run(os.getenv('TOKEN'))
app.run()
