import os

import discord
import google.generativeai as genai
from dotenv import load_dotenv


class geminni:
    load_dotenv()
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    system_prompt = "You are a helpful bot!"
    image_prompt = "You are a helpful bot!"
    text_generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 512,
    }
    image_generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 512,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    ]
    text_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=text_generation_config,
                                       safety_settings=safety_settings, system_instruction=system_prompt)
    image_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=image_generation_config,
                                        safety_settings=safety_settings, system_instruction=image_prompt)

    async def mandarPrompt(mensaje: str):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(mensaje)
        print(response.text)
        embed = discord.Embed(title="Respuesta de Gemini: ", description=response.text, color=discord.Color.green())
        return embed

    # ---------------------------------------------AI Generation History-------------------------------------------------

    async def generate_response_with_text(message_text):
        prompt_parts = [message_text]
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        # sanitized_text = message_text.encode('ascii', 'ignore').decode('ascii')
        # print("Got textPrompt: " + sanitized_text)
        response = geminni.text_model.generate_content(prompt_parts)
        if (response._error):
            return "X" + str(response._error)
        return response.text

    async def generate_response_with_image_and_text(image_data, text):
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], f"\n{text if text else 'De que seria esta foto?'}"]
        response = geminni.image_model.generate_content(prompt_parts)
        if (response._error):
            return "X" + str(response._error)
        return response.text
