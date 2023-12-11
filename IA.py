
from urllib.request import urlopen
from bs4 import BeautifulSoup
import discord

class IAimple:
  def generateFact(msj:str):
    print("Entro a el #generateFunFact")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generate?Entry="+msj
    htmlSinEspacios = htmlStart.replace(" ", "%20")
    html = urlopen(htmlSinEspacios).read()
    print("HTML OBTENIDO: "+htmlSinEspacios)
    unicode_str = html.decode('utf8')
    encoded_str = unicode_str.encode("utf8",'ignore')
    soup = BeautifulSoup(encoded_str,'html.parser')
    print("Voy a buscar el body con la clase especificada para obtener la data")
    divparent = soup.find('body', attrs={'class': 'dataPromp'})
    cadena=""""""
    for row in divparent.find_all('p'):
      cadena = str(row.text)
    embed = discord.Embed(title="Generate Fun Fact", description="Fun fact con IA", color=0x00ff00)
    embed.add_field(name="Prompt", value=msj, inline=False)
    embed.add_field(name="Texto generado", value=cadena, inline=False)
    responseTexto=cadena.strip()
    print("Response Obtenido: "+responseTexto)
    return embed
  
  
  def generate(msj:str):
    print("Entro a el #generate")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://generador-de-funfact-con-chatgpt4--facundoguerrero.repl.co/generateByPromt?Entry="+msj
    htmlSinEspacios = htmlStart.replace(" ", "%20")
    html = urlopen(htmlSinEspacios).read()
    print("HTML OBTENIDO: "+htmlSinEspacios)
    unicode_str = html.decode('utf8')
    encoded_str = unicode_str.encode("utf8",'ignore')
    soup = BeautifulSoup(encoded_str,'html.parser')
    print("Voy a buscar el body con la clase especificada para obtener la data")
    divparent = soup.find('body', attrs={'class': 'dataPromp'})
    cadena=""""""
    for row in divparent.find_all('p'):
      cadena = row.get_text()
    embed = discord.Embed(title="Generate", description="Texto generado con IA", color=0x00ff00)
    embed.add_field(name="Prompt", value=msj, inline=False)
    embed.add_field(name="Texto generado", value=cadena, inline=False)
    responseTexto=cadena
    print("Response Obtenido: "+responseTexto)
    
    return embed

  def generateImage(msj:str):
    print("Entro a el #generate imagen por IA")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://discordiaimg.facundoguerrero.repl.co/generateImagen?Entry="+msj
    htmlSinEspacios = htmlStart.replace(" ", "%20")
    html = urlopen(htmlSinEspacios).read()
    print("HTML OBTENIDO: "+htmlSinEspacios)
    soup = BeautifulSoup(html,'html5lib')
    print("Voy a buscar el body con la clase especificada para obtener la data")
    cadena=None
    for imgtag in soup.find_all('img'):
      cadena=imgtag['src']
    print("cadena obtenida: ",cadena)
    responseTexto=cadena
    embed = discord.Embed(title="Generate Image", description="Imagen generada con IA", color=0x00ff00)
    embed.add_field(name="Prompt", value=msj, inline=False)
    embed.set_image(url=cadena)
    print("Response Obtenido: ",responseTexto)
    return embed


  def generateImageOpenai(msj:str):
    print("Entro a el #generate imagen por OpenAI")
    responseTexto = ""
    print('Abriendo url para generar y llamar a la otra api.')
    htmlStart ="https://discordiaimg.facundoguerrero.repl.co/generateImagenOpenIA?Entry="+msj
    htmlSinEspacios = htmlStart.replace(" ", "%20")
    html = urlopen(htmlSinEspacios).read()
    print("HTML OBTENIDO: "+htmlSinEspacios)
    soup = BeautifulSoup(html,'html5lib')
    print("Voy a buscar el body con la clase especificada para obtener la data")
    cadena=None
    for imgtag in soup.find_all('img'):
      cadena=imgtag['src']
    print("cadena obtenida: ",cadena)
    embed = discord.Embed(title="Generate Image with OPEN IA", description="Imagen generada con IA - Dalle", color=0x00ff00)
    embed.add_field(name="Prompt", value=msj, inline=False)
    embed.set_image(url=cadena)
    responseTexto=cadena
    print("Response Obtenido: ",responseTexto)
    return embed