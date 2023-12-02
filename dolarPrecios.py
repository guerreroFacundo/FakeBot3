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


class findUsd:
  def obtenerDolar():
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
    return result


  def steam(arg:str):
    result = ""
    url = "https://www.dolarsi.com/api/dolarSiInfo.xml"
    response = urlopen(url)
    xml_data = response.read()
    data_dict = xmltodict.parse(xml_data)
    json_data = json.dumps(data_dict)
    data = json.loads(json_data)
    custom_value = data['cotiza']['valores_principales']['casa406']
    custom_value = custom_value.get('nombre')+':\n'+custom_value.get('compra')+'  Compra\n'+custom_value.get('venta')+' Venta'
    print(custom_value)
    customValor = data['cotiza']['valores_principales']['casa406']
    arg = arg.replace(',','.')
    valor = str(customValor.get('venta')).replace(',','.')
    calculado = float(valor) * float(arg)
    print(calculado)
    return result+"\n\n"+custom_value+"\n Valor steam: "+str(calculado)