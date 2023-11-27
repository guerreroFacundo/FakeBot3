# Bot para probar cosas randoms
import os
import typing
import discord
from discord import Embed
import random
from discord.ext import commands
from discord import app_commands
import xmltodict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import keep_alive
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
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



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



