from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from RemoveBG.service.remove import Remove
import os
from Master.settings import BASE_DIR
from RemoveBG.forms import ContactForm

# Create your views here.

def page_upload(request):
    context = {'key': 'value'}
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
            return remove.remove_bg(file_name)
        except:
            check_files_to_delete(file_name)
            return HttpResponse(f'Erro ao receber o arquivo', status=400)
    return HttpResponse(f'Erro ao receber o arquivo', status=400)


def contact_view(request):
    if request.method == 'POST':
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(f'Erro ao receber o arquivo', status=400)
        except:
            return HttpResponse(f'Erro ao receber o arquivo', status=400)
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})