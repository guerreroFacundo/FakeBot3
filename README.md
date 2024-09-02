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

### Despliegue Local como servicio con pm2

Comandos utilizados:
1. Instalar variables de entorno
   CREAR LA VARIABLE DE ENTORNO o Environment Variables
   ```bash
   pm2_home=c:\.pm2
   ```
2. Instalar y Desinstalar PM2
   ```bash
   npm install pm2 -g
   npm uni pm2 -g
   ```
3. Cargar app
   ```bash
   pm2 start D:/0backend/backend/build/index.js --name "DiscordBot"
   pm2 save
   pm2 start all
   ```
### Poner como servicio
```bash
npm install pm2-windows-service -g
pm2-service-install -n DiscordBot
```
**No configurar la linea siguiente por defecto**

--->PM2_SERVICE_SCRIPTS? No

### Desinstalar servicios
```bash
pm2-service-uninstall
npm uni pm2 -g
```
## Contribuciones

Este proyecto es principalmente para fines de aprendizaje, pero las contribuciones son bienvenidas. Si deseas mejorar el bot o agregar nuevas funcionalidades, siéntete libre de hacer un fork y enviar un pull request.


