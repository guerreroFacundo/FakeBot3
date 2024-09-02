# Importing libraries
import discord
import os
import asyncio
import youtube_dl
import time
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

queues = {}
estaAndando=False
# This event happens when a message gets sent
class music:
  async def play(msg: discord.Interaction,urlmsj:str):
    playlistString = "playlist"
    if(playlistString in urlmsj):
        print("Es una lista de reproduccion")
        respuesta = []
        respuesta = await urlextract.extract_urls(urlmsj)
        print("Respuesta: ",respuesta)
        voice_client = await msg.user.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
        for url in respuesta:
          
          print("URL: ",url)
          loop = asyncio.get_event_loop()
          print("Obtuve el loop vy a tirar : run_in_executor")
          data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
          print("Obtuve la data voy a obtener data['url']")
          song = data['url']
          print("cargue la variable song voy a cargarle lo siguiente: ",ffmpeg_options)
          player = discord.FFmpegOpusAudio(song,**ffmpeg_options)
          
          #Parte nueva---------------
          if voice_client.guild.id in queues:
            queues[voice_client.guild.id].append(player)
            print("ya se esta reproduciendo algo agrego player nuevo a la lista")
          else:
            queues[voice_client.guild.id]=[player]
            print("No se estaba reproduciendo nada lo agrego de una a la lista")
          print("Cargue el player")
          queues[voice_client.guild.id].pop(0)
          #----------------------------------
          estaAndando = voice_client.is_playing()
          print("El bot esta andando? : ",estaAndando)
          while voice_client.is_playing():
            if(not voice_client.is_playing()):
              print("Termino de reproducir")
          voice_clients[msg.guild.id].play(player)
          print("le di a play dentro de voice_clients")
    else:
        print("Es una cancion sola")
        try:
            voice_client = await msg.user.voice.channel.connect()
            print(f"Guild ID: {voice_client.guild.id}")
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as err:
            print("error al obtener voice_clientes: ",err)
            
        try:
            url = urlmsj
            print("URL: ",url)
            loop = asyncio.get_event_loop()
            print("Obtuve el loop vy a tirar : run_in_executor")
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            print("Obtuve la data voy a obtener data['url']")
            song = data['url']
            print("cargue la variable song voy a cargarle lo siguiente: ",ffmpeg_options)
            player = discord.FFmpegOpusAudio(song,**ffmpeg_options)
            print("Cargue el player")
            voice_clients[msg.guild.id].play(player)
            print("le di a play dentro de voice_clients")
        except Exception as err:
            print("Error al darle play a la url creo",err)
  


  

  
  async def pause(msg: discord.Interaction):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)
  
      # This resumes the current song playing if it's been paused
  async def resume(msg: discord.Interaction):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)
  
      # This stops the current playing song
  async def stop(msg: discord.Interaction):
      try:
          voice_clients[msg.guild.id].stop()
          await voice_clients[msg.guild.id].disconnect()
      except Exception as err:
          print(err)


class urlextract:
  async def extract_urls(urls:str):
  #extract playlist id from url

    query = parse_qs(urlparse(urls).query, keep_blank_values=True)
    playlist_id = query["list"][0]
  
    print(f'get all playlist items links from {playlist_id}')
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = os.getenv('GOOGLE_API_KEY'))
  
    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 50
    )
    response = request.execute()
  
    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)
  
    print(f"total: {len(playlist_items)}")
    print([ 
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&t=0s'
        for t in playlist_items
    ])
    urlsarmadas = []
    for t in playlist_items:
      urlsfalopa = str(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&t=0s')
      print("Url armada falopa: ",urlsfalopa)
      urlsarmadas.append(urlsfalopa) 
    print("URL dentro del array antes de pasarlo: ",urlsarmadas)
    return urlsarmadas

