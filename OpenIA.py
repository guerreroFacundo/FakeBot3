import json
import os

import aiohttp
import discord


class chatGPT:
    async def mandarPrompt(mensaje: str):
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "babbage-002",
                "prompt": mensaje,
                "temperature": 0.5,
                "max_tokens": 50,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1,
            }
            headers = {"Authorization": f"Bearer {os.getenv('OPENIA_API_KEY')}"}
            url = os.getenv('OPEN_IA_URL')
            async with session.post(url, json=payload, headers=headers) as resp:
                response = await resp.json()
                print(response)
                if "error" in response:
                    print("error devuelto por chatGPT")
                    embed = discord.Embed(title="Error: ", description=response["error"]["message"],colour=0xff0000)
                    embed.add_field(name="Tipo de error", value=response["error"]["type"])
                    return embed
                embed = discord.Embed(title="Chat GPT respuesta: ", description=response["choices"][0]["text"])
                return embed
