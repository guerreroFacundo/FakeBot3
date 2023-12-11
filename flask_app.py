from flask import Flask, render_template_string, render_template
from threading import Thread
from flask_cors import CORS, cross_origin
import discord
from discord import app_commands
import json

app = Flask('')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
intents = discord.Intents.all()
intents.message_content = True
intents.members = True



def cargarComandos():
  try:
    with open('comandos.json', 'r') as json_file:
      comand_data = json.load(json_file)
      return comand_data
  except FileNotFoundError:
    print("El archivo 'comandos.json' no se ha encontrado.")
    return {}


def run():
  app.run(host="0.0.0.0", port=8080)


def keep_alive():
  server = Thread(target=run)
  server.start()


if __name__ == '__main__':
  # Ejecutar el servidor Flask solo si se ejecuta directamente desde este archivo
  run()


@app.route('/', methods=['GET'])
@cross_origin()
def home():
  # Obtén la lista de comandos de tu variable 'tree'
  comandos_guardados = cargarComandos()
  return render_template('home.html', commands=comandos_guardados)


@app.route('/game', methods=['GET'])
def index():
  return render_template('game.html')
