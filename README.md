# Proyecto Personal - Bot en Python

Este es un proyecto personal que desarrollé para aprender y practicar Python. Se trata de un bot programado en Python que inicialmente fue desarrollado y hospedado en [Replit](https://replit.com/), pero que ahora se está ejecutando de manera local utilizando [PM2](https://pm2.keymetrics.io/), un gestor de procesos que permite ejecutar y mantener aplicaciones Node.js (y otros scripts) en producción.

## Descripción

El bot tiene como objetivo disponer de comandos que sean utiles en el dia a dia. Este proyecto me ha permitido mejorar mis habilidades en Python, así como aprender sobre el proceso de despliegue y administración de aplicaciones en un entorno de producción local.

## Instalación y Ejecución

### Requisitos

- Python 3.x
- PM2

### Pasos para la instalación

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Instalar las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```
3. Acordarse de crear un .env con los valores correspondientes

4. Configurar PM2 para ejecutar el bot:
    ```bash
    pm2 start bot.py --name "mi-bot"
    ```

5. Verificar que el bot esté corriendo:
    ```bash
    pm2 status
    ```

### Despliegue

El bot se despliega y se mantiene en ejecución localmente utilizando PM2. Esto asegura que el bot esté siempre activo y reinicie automáticamente en caso de errores o reinicios del sistema.

## Contribuciones

Este proyecto es principalmente para fines de aprendizaje, pero las contribuciones son bienvenidas. Si deseas mejorar el bot o agregar nuevas funcionalidades, siéntete libre de hacer un fork y enviar un pull request.


