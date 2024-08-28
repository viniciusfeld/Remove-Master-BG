from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.core.files.storage import default_storage
from RemoveBG.service.remove import Remove
from RemoveBG.service.send_email import DataEmail
import os
from Master.settings import BASE_DIR
from RemoveBG.forms import ContactForm
from django.conf import settings

from dotenv import load_dotenv
load_dotenv()

url_site = os.getenv('URL_SITE')

# Create your views here.

def page_upload(request):
    context = {'key': 'value', "URL_SITE": url_site}
    print("url_site no page upload", url_site)
    return render(request, 'index.html', context)


def check_files_to_delete(file_name):

    if os.path.exists(f"{BASE_DIR}/media/{file_name}"):
        os.remove(f"{BASE_DIR}/media/{file_name}")
    if os.path.exists(f"{BASE_DIR}/img_remove_bg/{file_name}_sem_fundo.png"):
        os.remove(f"{BASE_DIR}/img_remove_bg/{file_name}_sem_fundo.png")
    if os.path.exists(f"{BASE_DIR}/img_white_background/{file_name}_fundo_branco.jpg"):
        os.remove(f"{BASE_DIR}/img_white_background/{file_name}_fundo_branco.jpg")


def upload_file(request):
    remove = Remove()
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['file']
            file_name = default_storage.save(uploaded_file.name, uploaded_file)
            status_remove = remove.remove_bg(file_name)
            if status_remove.status_code == 200:
                request.session['file_name'] = file_name
                return JsonResponse({'redirect_url': reverse('download_file')})
            else:
                check_files_to_delete(file_name)
                return HttpResponse(f'Erro ao receber o arquivo', status=400)
        except Exception as e:
            print(f"Erro: {e}")
            check_files_to_delete(file_name)
            return HttpResponse(f'Erro ao receber o arquivo', status=400)
    return HttpResponse(f'Erro ao receber o arquivo', status=400)


def contact_view(request):
    if request.method == 'POST':
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
        except:
            return HttpResponse(f'Erro ao receber seu contato. Tente novamente', status=400)
        
        try:
            DataEmail.auto_email_contact_inside(request)
            return HttpResponse(f'Email enviado com sucesso', status=200)
        except Exception as e:
            print(f"Erro: {e}")
            return HttpResponse(f'Erro ao receber seu contato. Tente novamente', status=400)        
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form, "URL_SITE": url_site})


def download_file(request):
    file_name = request.session.get('file_name')
    download_url = f"{url_site}/serve_file/{file_name}"  # Ajuste conforme a configuração do seu site
    context = {'download_url': download_url, 'file_name': file_name, "URL_SITE": url_site}
    return render(request, 'file_download.html', context)


def serve_file(request, file_name):
    download_type = request.GET.get('type')    
    file_name = file_name.split('.')[0]

    if download_type == "jpg":
        file_name = f"{file_name}_fundo_branco.jpg"
        file_path = os.path.join(BASE_DIR, 'img_white_background', file_name)
    elif download_type == "png":
        file_name = f"{file_name}_sem_fundo.png"
        file_path = os.path.join(BASE_DIR, 'img_remove_bg', file_name)
    
    if not os.path.exists(file_path):
        raise Http404("Arquivo não encontrado")

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response
    
