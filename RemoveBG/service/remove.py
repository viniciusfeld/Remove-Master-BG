from PIL import Image
from rembg import remove
from Master.settings import BASE_DIR
from django.http import HttpResponse
import os
import time

class Remove():

    def insert_white_background(self, path_img, file_name):
        im = Image.open(path_img)

        fill_color = (255,255,255)  # your new background color

        im = im.convert("RGBA")   # it had mode P after DL it from OP
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], (1200, 1200), fill_color)
            x_position = (background.width - im.width) // 2
            y_position = (background.height - im.height) // 2
            background.paste(im, (x_position,y_position),im.split()[-1]) # omit transparency
            im = background
        
        path_img_white_bg = str(f"{BASE_DIR}/img_white_background/{file_name}_fundo_branco").replace(".png","") + '.jpg'
        im.convert("RGB").save(path_img_white_bg)
        
        return HttpResponse("Imagem criada com sucesso", status=200)

    def remove_bg(self, file_name):
        # Carregar imagem
        imagem = Image.open(f"{BASE_DIR}/media/{file_name}")
        desired_size = (1200, 1200)
        imagem.thumbnail(desired_size, Image.LANCZOS)

        # Remover fundo
        imagem_sem_fundo = remove(imagem, api_key="SEU_API_KEY")
        imagem_sem_fundo.thumbnail(desired_size, Image.LANCZOS)
        new_image = Image.new("RGBA", desired_size, (0, 0, 0, 0))
        position = ((desired_size[0] - imagem_sem_fundo.size[0]) // 2, (desired_size[1] - imagem_sem_fundo.size[1]) // 2)
        new_image.paste(imagem_sem_fundo,position)
        
        # Salvar como PNG e JPG
        path_img = f"{BASE_DIR}/img_remove_bg/{file_name}_sem_fundo.png"
        new_image.save(path_img)

        while not os.path.exists(path_img):
            time.sleep(1)
        os.remove(f"{BASE_DIR}/media/{file_name}")
        return self.insert_white_background(path_img, file_name)
