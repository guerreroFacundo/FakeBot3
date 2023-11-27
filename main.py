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
import keep_alive
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
MY_GUILD = discord.Object(id=1071229378576527492) 




class MyClient(discord.Client):
  def __init__(self, *, intents: discord.Intents):
      super().__init__(intents=intents)
      # A CommandTree is a special type that holds all the application command
      # state required to make it work. This is a separate class because it
      # allows all the extra state to be opt-in.
      # Whenever you want to work with application commands, your tree is used
      # to store and work with them.
      # Note: When using commands.Bot instead of discord.Client, the bot will
      # maintain its own tree instead.
      self.tree = app_commands.CommandTree(self)

  # In this basic example, we just synchronize the app commands to one guild.
  # Instead of specifying a guild to every command, we copy over our global commands instead.
  # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
  async def setup_hook(self):
      # This copies the global commands over to your guild.
      self.tree.copy_global_to(guild=MY_GUILD)
      await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print('Loggeado como: {0.user}'.format(client))




##COMANDO DE PRUEBA PARA QUE TE SALGA CON EL /
@client.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')



#COMANDO DE PRUEBA PARA QUE ME SALGA OTRO COMANDO PERO PARA MANDAR MSJ
@client.tree.command()
async def generate(interaction: discord.Interaction,message:str):
    await interaction.response.defer(thinking=True)
    print("Entro a el #generate")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generateByPromt?Entry="+message
    htmlSinEspacios = htmlStart.replace(" ", "%20")
    html = urlopen(htmlSinEspacios).read()
    print("HTML OBTENIDO: "+htmlSinEspacios)
    soup = BeautifulSoup(html,'html5lib')
    print("Voy a buscar el body con la clase especificada para obtener la data")
    divparent = soup.find('body', attrs={'class': 'dataPromp'})
    cadena=""""""
    for row in divparent.find_all('p'):
      cadena = str(row.text)
    responseTexto=cadena.strip()
    print("Response Obtenido: "+responseTexto)
    await interaction.followup.send(responseTexto)



#Cando dolar pero con el / jejeje
@client.tree.command()
async def dolar(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True)
  result = """"""
  responseTexto = ""
  print('Obteniendo cotización dolar')
  html = urlopen("https://dolarhoy.com/i/cotizaciones/dolar-blue").read()
  soup = BeautifulSoup(html,'html5lib')
  divparent = soup.find('div', attrs={'class': 'data__valores'})
  for row in divparent.find_all('p'):
    cadena = str(row.text)
    cadena=cadena.replace("Compra"," Compra")
    cadena=cadena.replace("Venta"," Venta")
    responseTexto=responseTexto+"\n"+cadena.strip()
  responseTexto = "Dolar Blue:"+responseTexto+"\n\nDolar MEP:"
  print('Obteniendo cotización dolar mep')
  html = urlopen("https://dolarhoy.com/i/cotizaciones/dolar-mep").read()
  soup = BeautifulSoup(html,'html5lib')
  divparent = soup.find('div', attrs={'class': 'data__valores'})
  for row in divparent.find_all('p'):
    cadena = str(row.text)
    cadena=cadena.replace("Compra"," Compra")
    cadena=cadena.replace("Venta"," Venta")
    responseTexto=responseTexto+"\n"+cadena.strip()
  result = responseTexto
  result ="\n\n"+result
  url = "https://www.dolarsi.com/api/dolarSiInfo.xml"
  response = urlopen(url)
  xml_data = response.read()
  data_dict = xmltodict.parse(xml_data)
  json_data = json.dumps(data_dict)
  data = json.loads(json_data)
  custom_value = data['cotiza']['Dolar']['casa344']
  custom_value = custom_value.get('nombre')+':\n'+custom_value.get('compra')+'  Compra\n'+custom_value.get('venta')+' Venta'
  print(custom_value)
  result=result+"\n\n"+custom_value
  custom_value = data['cotiza']['valores_principales']['casa406']
  custom_value = custom_value.get('nombre')+':\n'+custom_value.get('compra')+'  Compra\n'+custom_value.get('venta')+' Venta'
  print(custom_value)
  result=result+"\n\n"+custom_value
  await interaction.followup.send(result)



@client.event
async def on_message(message):
    if message.author == client.user:
        return

  
    #TEST DE HOLA
    if message.content.startswith('#hello'):
        await message.channel.send('Hello!')

  
    #TEST DE MENSAJE
    if message.content == '$mensaje' :
      randomTexts = ['Hello', 'How are you?', 'Have a great day!']
      randomIndex = random.randint(0, len(randomTexts)-1)
      await message.channel.send(randomTexts[randomIndex])

  
    ##ESTO TE DEVUELVE LOS VALORES DE LOS DOLARES
    if message.content.startswith('#dolar'):
      result = """
    """
      responseTexto = ""
      print('Obteniendo cotización dolar')
      html = urlopen("https://dolarhoy.com/i/cotizaciones/dolar-blue").read()
      soup = BeautifulSoup(html,'html5lib')
      divparent = soup.find('div', attrs={'class': 'data__valores'})
      for row in divparent.find_all('p'):
        cadena = str(row.text)
        cadena=cadena.replace("Compra"," Compra")
        cadena=cadena.replace("Venta"," Venta")
        responseTexto=responseTexto+"\n"+cadena.strip()
      responseTexto = "Dolar Blue:"+responseTexto+"\n\nDolar MEP:"
      print('Obteniendo cotización dolar mep')
      html = urlopen("https://dolarhoy.com/i/cotizaciones/dolar-mep").read()
      soup = BeautifulSoup(html,'html5lib')
      divparent = soup.find('div', attrs={'class': 'data__valores'})
      for row in divparent.find_all('p'):
        cadena = str(row.text)
        cadena=cadena.replace("Compra"," Compra")
        cadena=cadena.replace("Venta"," Venta")
        responseTexto=responseTexto+"\n"+cadena.strip()
      result = responseTexto
      result ="\n\n"+result
      url = "https://www.dolarsi.com/api/dolarSiInfo.xml"
      response = urlopen(url)
      xml_data = response.read()
      data_dict = xmltodict.parse(xml_data)
      json_data = json.dumps(data_dict)
      data = json.loads(json_data)
      custom_value = data['cotiza']['Dolar']['casa344']
      custom_value = custom_value.get('nombre')+':\n'+custom_value.get('compra')+'  Compra\n'+custom_value.get('venta')+' Venta'
      print(custom_value)
      result=result+"\n\n"+custom_value
      custom_value = data['cotiza']['valores_principales']['casa406']
      custom_value = custom_value.get('nombre')+':\n'+custom_value.get('compra')+'  Compra\n'+custom_value.get('venta')+' Venta'
      print(custom_value)
      result=result+"\n\n"+custom_value
      await message.channel.send(result)



  
    ##ESTE ES EL GENERATE FUN FACT PARA QUE TE GENERE UN DATO SOBRE LO QUE LE MANDES
    if message.content.startswith('#generateFunFact'):
        print("Entro a el #generateFunFact")
        responseTexto = ""
        print('Abriendo url para generar y llamar a la otra api.')
        htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generate?Entry="+message.content[16:]
        htmlSinEspacios = htmlStart.replace(" ", "%20")
        html = urlopen(htmlSinEspacios).read()
        print("HTML OBTENIDO: "+htmlSinEspacios)
        soup = BeautifulSoup(html,'html5lib')
        print("Voy a buscar el body con la clase especificada para obtener la data")
        divparent = soup.find('body', attrs={'class': 'dataPromp'})
        cadena=""""""
        for row in divparent.find_all('p'):
          cadena = str(row.text)
        
        responseTexto=cadena.strip()
        print("Response Obtenido: "+responseTexto)
        await message.channel.send(responseTexto)


  
    ##ESTE ES EL GENERATE PARA QUE GENERE CUALQUIER COSA QUE LE MANDES LUEGO DEL COMANDO
    if message.content.startswith('#generate'):
      print("Entro a el #generate")
      responseTexto = ""
      print('Abriendo url para generar y llamar a la otra api.')
      htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generateByPromt?Entry="+message.content[9:]
      htmlSinEspacios = htmlStart.replace(" ", "%20")
      html = urlopen(htmlSinEspacios).read()
      print("HTML OBTENIDO: "+htmlSinEspacios)
      soup = BeautifulSoup(html,'html5lib')
      print("Voy a buscar el body con la clase especificada para obtener la data")
      divparent = soup.find('body', attrs={'class': 'dataPromp'})
      cadena=""""""
      for row in divparent.find_all('p'):
        cadena = str(row.text)

      responseTexto=cadena.strip()
      print("Response Obtenido: "+responseTexto)
      await message.channel.send(responseTexto)







      
keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))
app.run()



