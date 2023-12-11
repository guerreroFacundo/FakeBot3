from steam import Steam
from steam import Apps as apsteam
from decouple import config
import json
import discord
import os
from datetime import datetime

class steam:
  def serch_player(player:str):
    response=""
    data=""
    steam = Steam(os.getenv('STEAM_API_KEY'))
    colores=discord.Colour.random()
    embed=discord.Embed(title="Steam Player Search", description="", color=colores)
    try:
      response=steam.users.search_user(player)
      json_data = json.dumps(response)
      data = json.loads(json_data)
      if(data=="No match"):
        embed = discord.Embed(title=f"No tenes URL personalizada en tu perfil, ingresa aca para hacerlo: https://steamcommunity.com/id/{player}/edit/info/info", description="", color=colores)
      else:
        custom_value = data['player']
        embed = discord.Embed(title=f"Steam profile: {player}", description="", color=colores)
        ts = datetime.utcfromtimestamp(custom_value['timecreated']).strftime('%Y-%m-%d %H:%M:%S')
        embed.add_field(name="Cuenta creada: ", value=f"{ts}", inline=True)
        responsegames=steam.users.get_user_recently_played_games(custom_value['steamid'])
        json_data = json.dumps(responsegames)
        datagames = json.loads(json_data)
        value_games = datagames["games"]
        nombresjuegos =[]
        for game in value_games:
          precioofthisgame =""
          preciofinalofthisgame =""
          discount_percent = "No tiene descuento"
          precio_juego = steam.apps.get_app_details(app_id=game['appid'],filters="price_overview")
          json_dataprecio = json.dumps(precio_juego)
          data_precio = json.loads(json_dataprecio)
          print(data_precio)
          for game_id, game_data in data_precio.items():
            if 'price_overview' in game_data['data']:
              if game_data['data']['price_overview']['initial_formatted'] != "":
                precioofthisgame = game_data['data']['price_overview']['initial_formatted']
              else:
                precioofthisgame = game_data['data']['price_overview']['final_formatted']
              preciofinalofthisgame = game_data['data']['price_overview']['final_formatted']
              if game_data['data']['price_overview']['discount_percent'] != 0:
                discount_percent ="%"+str(game_data['data']['price_overview']['discount_percent'])
              print(f"El precio final formateado para el juego con ID {game_id} es: {precioofthisgame}")
            else:
                print(f"No hay información de precio disponible para el juego con ID {game_id}")
                precioofthisgame = "El Juego es gratis"
                discount_percent = "No tiene descuento"
                preciofinalofthisgame = "El Juego es gratis"
          resultado_juego = steam.apps.get_app_details(app_id=game['appid'])
          json_data = json.dumps(resultado_juego)
          data_juego = json.loads(json_data)
          for datavalor in data_juego.items():
            for datito in datavalor:
              for datito2 in datito:
                if(datito2=="data"):
                  print(datito['data']['capsule_imagev5'])
                  embed.add_field(name=f"Juego recientemente jugado: ", value=f"Nombre: {game['name']} \n Tiempo de juego: {int(game['playtime_forever'])/60}  \n Precio: {precioofthisgame} \n Descuento: {discount_percent} \n Precio final: {preciofinalofthisgame} ", inline=False)
        embed.add_field(name=f"URL personalizada: ", value=f"https://steamcommunity.com/id/{player}",inline=True)
        
        embed.set_image(url=custom_value['avatarfull'])
          
    except Exception as err:
      print("DIO ERROR")
      print(err)
      embed = discord.Embed(title=f"Error al buscar usuario: {player}", description=f"{err}", color=colores)
    
    

    return embed
