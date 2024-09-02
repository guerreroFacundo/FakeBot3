from PIL import Image
from io import BytesIO
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import discord


class imagenes:
  async def armarImagenBonk2(interaction: discord.Interaction,member: discord.Member):
    print("Armando imagen bonk 2")
    
    # Abrir la imagen bonkBien.jpg
    my_image = Image.open("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/bonkBien.jpg")

    # Obtener la imagen del avatar de interaction.user
    asset = interaction.user.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((400, 300))
    my_image.paste(pfp, (450, 90))

    # Guardar la imagen temporal
    my_image.save("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/temp_profile.png")

    # Abrir la imagen perritobonkeado.jpg
    image_perrito = Image.open("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/perritobonkeado.jpg")

    # Obtener la imagen del avatar de member
    avatar_usuario = member.display_avatar
    data_avatar_usuario = BytesIO(await avatar_usuario.read())
    pfp_avatar_usuario = Image.open(data_avatar_usuario)
    pfp_avatar_usuario = pfp_avatar_usuario.resize((250, 250))
    image_perrito.paste(pfp_avatar_usuario, (90, 150))

    # Guardar la imagen final
    image_perrito.save("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/perfil_final.png")

    # Abrir las imágenes temporales y finales
    image_temp_profile = Image.open("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/temp_profile.png")
    image_perfil_final = Image.open("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/perfil_final.png")

    # Redimensionar las imágenes para asegurar que ambas se vean completamente
    image_temp_profile = image_temp_profile.resize((500, 500))
    image_perfil_final = image_perfil_final.resize((300, 500))

    # Crear una nueva imagen combinada con las dimensiones totales
    image_combinada = Image.new("RGBA", (image_temp_profile.width + image_perfil_final.width, max(image_temp_profile.height, image_perfil_final.height)))

    # Pegar ambas imágenes en la imagen combinada
    #image_combinada.paste(image_temp_profile, (0, 0))
    image_combinada.paste(image_perfil_final, (image_temp_profile.width-200, 0))
    image_combinada.paste(image_temp_profile, (0, 0),mask=image_temp_profile)

    
    
    
    # Guardar la imagen final combinada
    image_combinada.save("F:/Archivos/Documentos/Proyectos - BPM - Intelijei - etc/FakeBot3/imagenes/perfil_completo.png")
    
    print("Termino de armar imagen bonk 2")
