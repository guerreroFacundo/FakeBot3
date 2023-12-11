
import xmltodict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import discord


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

  def obtenerDolar2():
    result = ""
    responseTexto = ""

    # Obtener cotización de Dólar Blue
    print('Obteniendo cotización dolar')
    html = urlopen("https://dolarhoy.com/i/cotizaciones/dolar-blue").read()
    soup = BeautifulSoup(html, 'html5lib')
    divparent = soup.find('div', attrs={'class': 'data__valores'})
    for row in divparent.find_all('p'):
        cadena = str(row.text)
        cadena = cadena.replace("Compra", " Compra")
        cadena = cadena.replace("Venta", " Venta")
        responseTexto = responseTexto + "\n" + cadena.strip()

    # Guardar los valores de Dólar Blue
    dolar_blue_compra = responseTexto.split()[0]
    dolar_blue_venta = responseTexto.split()[2]

    responseTexto = ""

    # Obtener cotización de Dólar MEP
    print('Obteniendo cotización dolar mep')
    html = urlopen("https://dolarhoy.com/i/cotizaciones/dolar-mep").read()
    soup = BeautifulSoup(html, 'html5lib')
    divparent = soup.find('div', attrs={'class': 'data__valores'})
    for row in divparent.find_all('p'):
        cadena = str(row.text)
        cadena = cadena.replace("Compra", " Compra")
        cadena = cadena.replace("Venta", " Venta")
        responseTexto = responseTexto + "\n" + cadena.strip()

    # Guardar los valores de Dólar MEP
    dolar_mep_compra = responseTexto.split()[0]
    dolar_mep_venta = responseTexto.split()[2]

    result = responseTexto
    result = "\n\n" + result
    url = "https://www.dolarsi.com/api/dolarSiInfo.xml"
    response = urlopen(url)
    xml_data = response.read()

    # Obtener valores oficiales usando json
    data_dict = xmltodict.parse(xml_data)
    json_data = json.dumps(data_dict)
    data = json.loads(json_data)

    # Obtener cotización de Dólar Oficial
    dolar_oficial_compra = data['cotiza']['Dolar']['casa344']['compra']
    dolar_oficial_venta = data['cotiza']['Dolar']['casa344']['venta']

    # Obtener cotización de Dólar Turista
    dolar_turista_compra = data['cotiza']['valores_principales']['casa406']['compra']
    dolar_turista_venta = data['cotiza']['valores_principales']['casa406']['venta']

    # Crear un embed para mostrar la información
    embed = discord.Embed(title='Cotización del Dólar', color=0x00ff00)
    embed.add_field(name='Dólar Blue', value=f'Compra: {dolar_blue_compra}\nVenta: {dolar_blue_venta}', inline=False)
    embed.add_field(name='Dólar MEP', value=f'Compra: {dolar_mep_compra}\nVenta: {dolar_mep_venta}', inline=False)
    embed.add_field(name='Dólar Oficial', value=f'Compra: {dolar_oficial_compra}\nVenta: {dolar_oficial_venta}', inline=False)
    embed.add_field(name='Dólar Turista', value=f'Compra: {dolar_turista_compra}\nVenta: {dolar_turista_venta}', inline=False)
    return embed
  
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