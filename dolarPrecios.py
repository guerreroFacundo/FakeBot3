import os
from datetime import datetime, timezone

import aiohttp
import discord
from dotenv import load_dotenv

class CustomAPIError(Exception):
    """Excepción personalizada para errores de API"""
    pass

class findUsd:
    load_dotenv()
    async def steam(dolarIngresado: str):
        # Convertimos 'pesos' a un número
        dolarIngresado = float(dolarIngresado.replace(',', '.'))
        urlDolar = os.getenv("DOLAR_API_IMPUESTITO_COMPLETO_URL")
        urlImpuestos = os.getenv("IMPUESTOS_API_URL")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(urlImpuestos) as res:
                    if res.status == 200:
                        impuestos = await res.json()
                        print(impuestos)
                    else:
                        print(f"Error al obtener impuestos: {res.status}")
                        raise CustomAPIError(f"Error al obtener impuestos: Código de estado {res.status}")
                async with session.get(urlDolar) as res:
                    if res.status == 200:
                        dolar = await res.json()
                        print(dolar['bancos'])
                    else:
                        print(f"Error al obtener el dólar: {res.status}")
                        raise CustomAPIError(f"Error al obtener el dólar: Código de estado {res.status}")
            except aiohttp.ClientError as e:
                raise CustomAPIError(f"Error en la solicitud: {e}")
        precioPorDolar = dolarIngresado * float(dolar['bancos']['sell'])
        print(f"precioPorDolar: {precioPorDolar}")
        print(f"precioPorDolar+Impuestos: {precioPorDolar * impuestos['overflowSum']}")
        print(f"precioPorDolar+ImpuestosPais de impuestito(falopa pero lo agrego por que queda relativamente parecido a lo que cobran): {precioPorDolar*0.08}")
        precioConImpuestos = precioPorDolar + (precioPorDolar * impuestos['overflowSum'])+(precioPorDolar*0.08)
        print(f"precioConImpuestos: {precioConImpuestos}")
        embed = discord.Embed(title='Dolar a Pesos para Steam', color=0x00ff00)
        embed.add_field(name="Precio Ingresado", value=f"{dolarIngresado:.2f}")
        embed.add_field(name="Dolar bancos", value=f"{dolar['bancos']['sell']}")
        embed.add_field(name="Precio Final", value=f"{precioConImpuestos:.2f}")
        return embed

    async def obtenerDolar3():
        url = os.getenv("DOLAR_API_URL")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                data = await res.json()
                # Crear un embed para mostrar la información
                embed = discord.Embed(title='Cotización del Dólar', color=0x00ff00)

                # Iterar sobre cada tipo de dólar en los datos
                for dolar in data:
                    nombre = dolar['nombre']
                    compra = dolar['compra']
                    venta = dolar['venta']
                    fecha = dolar['fechaActualizacion']

                    # Agregar la información como un campo en el embed
                    embed.add_field(name=f"Dolar {nombre}",
                                    value=f"Compra: {compra}\nVenta: {venta}\nActualizado: {fecha}",
                                    inline=False)

                return embed

    def timestamp_to_local(timestamp_ms):
        timestamp_s = timestamp_ms / 1000  # Convertir milisegundos a segundos
        dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)  # Convertir a datetime en UTC
        local_dt = dt.astimezone()  # Convertir a la zona horaria local
        return local_dt.strftime('%d/%m/%Y %H:%M:%S')  # Formato de fecha y hora

    async def obtenerDolar4():
        url = os.getenv("DOLAR_API_IMPUESTITO_COMPLETO_URL")
        # Tipos de dólar que queremos mostrar
        selected_types = ['informal', 'mep', 'oficial', 'tarjeta']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        # Crea un embed para mostrar la información
        embed = discord.Embed(title="Cotizaciones del Dólar", color=discord.Color.blue())

        for key in selected_types:
            value = data.get(key, {})
            name = value.get('name', 'Desconocido').replace('dolar', 'Dólar')
            buy = value.get('buy', 'N/A')
            sell = value.get('sell', 'N/A')
            variation = value.get('variation', 'N/A')
            spread = value.get('spread', 'N/A')
            timestamp = value.get('timestamp', None)
            timestamp_local = findUsd.timestamp_to_local(timestamp) if timestamp else 'N/A'

            embed.add_field(
                name=name,
                value=f"Compra: {buy}\nVenta: {sell}\nVariación: {variation}\nSpread: {spread}\nFecha: {timestamp_local}",
                inline=False
            )
        return embed
