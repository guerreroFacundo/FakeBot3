import os

import aiohttp
import discord
from datetime import date, timedelta

from dotenv import load_dotenv


class clima:
    load_dotenv()
    async def obtenerClima(ciudad: str):
        url = os.getenv('WEATHER_API_URL')
        params = {
            "key": os.getenv('WEATHER_API_KEY'),
            "q": ciudad,
            "lang": "es"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                data = await res.json()

                location = data["location"]["name"]
                temp_c = data["current"]["temp_c"]
                humedad = data["current"]["humidity"]
                viento = data["current"]["wind_kph"]
                nubes = data["current"]["cloud"]
                temperatura_sensacion = data["current"]["feelslike_c"]
                isDay = data["current"]["is_day"]
                fechaDeActualizacion = data["current"]["last_updated"]
                condicion = data["current"]["condition"]["text"]
                condicionIcon = "http:" + data["current"]["condition"]["icon"]
                estado_del_dia = "Es de día" if isDay == 1 else "Es de noche"
                embed = discord.Embed(title=f"Clima para {location}",
                                      description=f"Las condiciones en {location} son {condicion}")
                embed.add_field(name="Ultima actualizacion", value=f"{fechaDeActualizacion}")
                embed.add_field(name="Temperatura", value=f"C: {temp_c}")
                embed.add_field(name="Sensación térmica", value=f"{temperatura_sensacion}")
                embed.add_field(name="Humedad", value=f"{humedad}")
                embed.add_field(name="Viento", value=f"KPH: {viento}")
                embed.add_field(name=estado_del_dia, value="")
                embed.set_thumbnail(url=condicionIcon)
                print("voy a retonar el embed")
                return embed




    async def obtenerClimaFuture(ciudad: str):
        print("INICIO obtenerClimaFuture")
        url = os.getenv('WEATHER_API_URL_FUTURE')
        hoy = date.today()
        # Sumar 14 días
        fecha_futura = hoy + timedelta(days=14)
        # Convertir la fecha en string con formato
        fecha_futura_str = fecha_futura.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
        params = {
            "key": os.getenv('WEATHER_API_KEY'),
            "q": ciudad,
            "dt": fecha_futura_str,
            "lang": "es"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                data = await res.json()

                # Datos de la ubicación
                location = data["location"]["name"]

                # Lista para almacenar los embeds
                embeds = []

                # Recorremos cada día de pronóstico
                for dia in data["forecast"]["forecastday"]:
                    fecha = dia["date"]

                    # Crear un embed para el pronóstico diario
                    embed_diario = discord.Embed(
                        title=f"Clima para {location} - {fecha}",
                        description=f"Condiciones en {location} para el {fecha}"
                    )
                    embed_diario.add_field(name="Temperatura Máxima", value=f"{dia['day']['maxtemp_c']}°C")
                    embed_diario.add_field(name="Temperatura Mínima", value=f"{dia['day']['mintemp_c']}°C")
                    embed_diario.add_field(name="Temperatura Promedio", value=f"{dia['day']['avgtemp_c']}°C")
                    embed_diario.add_field(name="Viento Máximo", value=f"{dia['day']['maxwind_kph']} KPH")
                    embed_diario.add_field(name="Precipitación Total", value=f"{dia['day']['totalprecip_mm']} mm")
                    embed_diario.add_field(name="Humedad Promedio", value=f"{dia['day']['avghumidity']}%")
                    embed_diario.set_thumbnail(url="http:" + dia['day']['condition']['icon'])

                    # Agregar el embed del pronóstico diario a la lista de embeds
                    embeds.append(embed_diario)
                    # Limitar a los primeros 10 horarios
                    primeras_10_horas = dia["hour"][:10]
                    # Recorremos cada hora del día
                    for hora in primeras_10_horas:
                        hora_tiempo = hora["time"]
                        temp_c = hora["temp_c"]
                        condicion_hora = hora["condition"]["text"]
                        condicionIcon_hora = "http:" + hora["condition"]["icon"]
                        humedad = hora["humidity"]
                        viento_kph = hora["wind_kph"]
                        precip_mm = hora["precip_mm"]

                        # Crear un embed para la hora
                        embed_hora = discord.Embed(
                            title=f"Clima por Hora - {hora_tiempo}",
                            description=f"Condiciones en {location} para el {fecha} a las {hora_tiempo}"
                        )
                        embed_hora.add_field(name="Temperatura", value=f"{temp_c}°C")
                        embed_hora.add_field(name="Condición", value=condicion_hora)
                        embed_hora.add_field(name="Humedad", value=f"{humedad}%")
                        embed_hora.add_field(name="Viento", value=f"{viento_kph} KPH")
                        embed_hora.add_field(name="Precipitación", value=f"{precip_mm} mm")
                        embed_hora.set_thumbnail(url=condicionIcon_hora)

                        # Agregar el embed de la hora a la lista de embeds
                        embeds.append(embed_hora)
                    # Si se han alcanzado los 10 embeds, detener la creación de más
                    if len(embeds) >= 10:
                        break

                # Solo devolver los primeros 10 embeds en caso de que se haya excedido el límite
                print("FIN obtenerClimaFuture")
                return embeds[:10]

