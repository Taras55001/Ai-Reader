"""
The module provides work with user files: uploading, saving, deketing, text extraction
"""
from django.shortcuts import render, redirect
import pickle
from django.http import HttpResponse
from .models import UploadedFile
from django.urls import reverse
from pypdf import PdfReader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from django.core.files import File as DjangoFile
from django.contrib import messages

from django.views.generic.edit import FormView
from .forms import FileFieldForm
import docx2python


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "pdf/upload_file.html"
    success_url = "pdf:upload_file"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("users:eror_aut"))
        form = FileFieldForm()
        return render(
            self.request,
            "pdf/upload_file.html",
            {
                "form": form,
                "files": UploadedFile.objects.filter(user_id=request.user.id),
            },
        )

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        """
        The form is being checked. If the form is correct and the uploaded file contains text, the data is processed and recorded in the database
        """
        files = form.cleaned_data["file_field"]
        for uploaded_file in files:
            if is_valid_type(uploaded_file):
                title = uploaded_file.name.split(".")[0]
                # reader = PdfReader(uploaded_file)
                text = ""
                text = get_text_from_file(uploaded_file)
                if text == "":
                    messages.error(
                        request, "Текст має нульову довжину. Введіть дійсний текст."
                    )
                    return redirect("pdf:upload_file")
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=200
                )
                chunks = text_splitter.split_text(text)
                embeddings = SentenceTransformerEmbeddings(
                    model_name="all-MiniLM-L6-v2"
                )
                vector_db = FAISS.from_texts(chunks, embeddings)
                with open(f"media/{title}.pkl", "wb") as f:
                    pickle.dump(vector_db, f)
                    vector_db_file = DjangoFile(
                        open(f"media/{title}.pkl", "rb"), name=f"{title}.pkl"
                    )
                    uploaded_file_obj = UploadedFile(
                        file=uploaded_file,
                        vector_db=vector_db_file,
                        user_id=self.request.user,
                    )
                uploaded_file_obj.save()

        return redirect("pdf:upload_file")


def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(
        uploaded_file.file, content_type="application/force-download"
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{uploaded_file.file.name}"'
    return response


def delete_file(request, file_id):
    """
    The procedure deletes file by id
    
    :param request: The HTTP request object.
    :type request: HttpRequest
    :param file_id: File id.
    :return: The HTTP response redirection
    :rtype: HttpResponseRedirect
"""
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    uploaded_file.file.delete()
    uploaded_file.delete()
    return redirect("pdf:upload_file")


def is_valid_type(file):
    """
    The procedure checks whether the downloaded file is supported
    
    :param file_name: The file to process
    :type file_name: InMemoryUploadedFile
    :return: True if file is supported
    :rtype: Bool
"""
    file_name = file.name

    file_extension = file_name.split(".")[-1].lower()
    if file_extension == "pdf" or file_extension == "docx" or file_extension == "txt":
        return True
    else:
        return False


def get_text_from_pdf(file_name, show_text: bool = False):
    """
    Returns text from .pdf file

    :param file_name: The file to process
    :type file_name: InMemoryUploadedFile
    :return: text from file
    :rtype: str
    """
    full_text = []
    try:
        reader = PdfReader(file_name)
        for page in reader.pages:
            text = page.extract_text()
            if show_text:
                print(text)
            full_text.append(text)
    except:
        full_text = []

    return "\n".join(full_text)


def get_text_from_docx(file_name):
    """
    Returns text from .docx file

    :param file_name: The file to process
    :type file_name: InMemoryUploadedFile
    :return: text from file
    :rtype: Str
    """
    res = ""
    try:
        docx = docx2python.docx2python(file_name)
        res = docx.text
    except:
        res = ""
    return res


def get_text_from_txt(file_name):
    """
    Returns text from .txt file. 

    :param file_name: The file to process
    :type file_name: InMemoryUploadedFile
    :return: text from file
    :rtype: str
    """
    try:
        file_text = ""

        for f_line in file_name:
            file_text += f_line.decode()
    except:
        file_text = ""

    return file_text


def get_text_from_file(file_name):
    """
    Returns text from file

    :param file_name: The file to process
    :type file_name: InMemoryUploadedFile
    :return: text from file
    :rtype: str
    """
    ext = file_name.name.split(".")[-1].lower()

    if ext == "docx":
        file_text = get_text_from_docx(file_name)
    elif ext == "pdf":
        file_text = get_text_from_pdf(file_name)
    elif ext == "txt":
        file_text = get_text_from_txt(file_name)
    else:
        file_text = ""

    return file_text
