from PIL import Image
# from rembg import remove
from Master.settings import BASE_DIR
from django.http import JsonResponse
import os
import time
import requests

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

        file_name_without_extension = file_name.split('.')[0]
        
        path_img_white_bg = str(f"{BASE_DIR}/img_white_background/{file_name_without_extension}_fundo_branco").replace(".png","") + '.jpg'
        im.convert("RGB").save(path_img_white_bg)
        
        return JsonResponse({"message": "Imagem criada com sucesso", "data": file_name}, status=200)

    def remove_bg(self, file_name):
        url = "https://api.remove.bg/v1.0/removebg"  # Endpoint para Remove.bg
        api_key = "Vtn1xgr46JJMHLdomBZP4Lyo"  # Substitua pela sua chave de API do Remove.bg

        # Carregar imagem
        input_image_path = f"{BASE_DIR}/media/{file_name}"
        desired_size = (1200, 1200)

        with open(input_image_path, 'rb') as image_file:
            headers = {
                'X-Api-Key': api_key
            }
            files = {
                'image_file': image_file
            }
            response = requests.post(url, headers=headers, files=files, stream=True)
            
            if response.status_code == 200:
                # Salvar a imagem com o fundo removido
                file_name_without_extension = file_name.split('.')[0]
                path_img = f"{BASE_DIR}/img_remove_bg/{file_name_without_extension}_sem_fundo.png"
                with open(path_img, 'wb') as out_file:
                    out_file.write(response.content)
                    out_file.close()

                # Garantir que o arquivo foi salvo antes de remover o original
                time.sleep(2)  # Adicionar atraso para garantir que o arquivo esteja disponível

                # Remover imagem original
                # if os.path.exists(input_image_path):
                #     os.remove(input_image_path)

                print(f"Removendo imagem com fundo removido: {path_img}")
                return self.insert_white_background(path_img, file_name)
            else:
                print(f'Erro: {response.status_code}')
                print(response.text)
                return JsonResponse({"message": "Erro ao remover fundo"}, status=response.status_code)