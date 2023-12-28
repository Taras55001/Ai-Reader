from django.shortcuts import render, redirect
import os
import mimetypes
from django.http import HttpResponse
from .models import UploadedFile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from pypdf import PdfReader 

from django.views.generic.edit import FormView
from .forms import FileFieldForm


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "pdf/upload_file.html"  
    success_url = "pdf:upload_file"  

    def get(self,request, *args, **kwargs):
        if  not request.user.is_authenticated:
            return redirect(reverse('users:eror_aut')) 
        form = FileFieldForm()
        return render(
            self.request, 
            'pdf/upload_file.html', 
            {'form': form, 'files': UploadedFile.objects.filter(user_id=request.user.id)}
        )
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for uploaded_file in files:
            if is_pdf(uploaded_file):
                title = uploaded_file.name.split('.')[0]
                reader = PdfReader(uploaded_file) 
                page = reader.pages[0] 
                print(title)
                text = page.extract_text() 
                print(text) 
                page = reader.pages[0]
                text = page.extract_text()

                uploaded_file_obj = UploadedFile(
                    file=uploaded_file,
                    user_id=self.request.user
                )
                uploaded_file_obj.save()
        return redirect('pdf:upload_file') 


def is_pdf(file):
    file_name = file.name

    file_extension = file_name.split('.')[-1].lower()
    if file_extension == 'pdf':
        return True
    else:
        return False



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


