from django.shortcuts import render, redirect
import os
import mimetypes
from django.http import HttpResponse
from .models import UploadedFile
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from pypdf import PdfReader 

def is_pdf(file):
    file_name = file.name

    file_extension = file_name.split('.')[-1].lower()
    if file_extension == 'pdf':
        return True
    else:
        return False


def upload_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.save(commit=False)
                if is_pdf(file.file):
                        file.user_id = request.user
                        file.save()
                        uploaded_file = request.FILES['file']
                        reader = PdfReader(uploaded_file) 
                        page = reader.pages[0] 
                        title=request.FILES['file'].name.split('.')[0]
                        print(title)
                        text = page.extract_text() 
                        print(text) 
                        return redirect('pdf:upload_file') 
                else:
                    return render(request, 'pdf/upload_file.html', {'form': form, 'files': UploadedFile.objects.all(), 'error_message': 'Файл має бути у форматі PDF'})
        else:
            form = UploadFileForm()
        files = UploadedFile.objects.filter(user_id=request.user.id)
        return render(request, 'pdf/upload_file.html', {'form': form, 'files': files})
    else:
        return redirect(reverse('users:eror_aut')) 





def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response

def delete_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    uploaded_file.file.delete()
    uploaded_file.delete()
    return redirect('pdf:upload_file')


