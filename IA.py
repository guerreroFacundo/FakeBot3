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
import json, requests

class IAimple:
  def generateFact(msj:str):
    print("Entro a el #generateFunFact")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generate?Entry="+msj
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
    return responseTexto
  
  
  def generate(msj:str):
    print("Entro a el #generate")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generateByPromt?Entry="+msj
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
    return responseTexto
    