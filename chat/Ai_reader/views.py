from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Chat, Message
from .model_answer import answer as ans
from pdf.models import UploadedFile
from .forms import ChooseFileForm
from django.http import HttpResponse
from django.contrib import messages


def main(request):
    return render(request, "Ai_reader/main.html")


def chat(request):
    user = request.user
    if request.user.is_authenticated:
        user_files = UploadedFile.objects.filter(user_id=request.user)
        user_chats = Chat.objects.filter(users=user)
        x = []
        for chat in user_chats:
            x.append(chat.name)

        return render(
            request,
            "Ai_reader/chat.html",
            {
                "user_chats": x,
                "user_files": user_files,
                "form": ChooseFileForm(user=user),
            },
        )

    else:
        return redirect(reverse("users:eror_aut"))


def ex_chat(request, chat_name):
    user = request.user
    if request.user.is_authenticated:
        user_chats = Chat.objects.filter(users=user)
        user_files = UploadedFile.objects.filter(user_id=request.user)
        x = []
        for chat in user_chats:
            x.append(chat.name)
        current_chat = user_chats.get(name=chat_name, users_id=user.id)
        user_file = current_chat.doc

        chat_replies = Message.objects.filter(chat=current_chat).order_by("created_at")


        return render(
            request,
            "Ai_reader/ex_chat.html",
            {
                "user_chats": x,
                "file": user_file,
                "current_chat": current_chat,
                "chat_replies": chat_replies,
                "user_files": user_files,
                # "form": ChooseFileForm(user=user),
            },
        )
    else:
        return redirect(reverse("users:eror_aut"))


def answer(request):
    if request.method == "POST":
        file = request.POST.get("file")
        print(file)
        user = request.user
        user_file = UploadedFile.objects.filter(id=file)
        if not user_file:
            messages.error(request, "Please upload a file fo context")
            return redirect("pdf:upload_file")
        message = request.POST.get("message")
        answer = ans(user_file[0], message)
        print(answer)
        chat_name = user_file[0].file.name
        name = chat_name.split(".")[0].lower()
        try:
            chat = Chat.objects.get(name=name, users=user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(
                name=name, users=user, doc=UploadedFile.objects.get(id=file)
            )
        chat = Chat.objects.get(name=name, users=user)
        user_message = Message.objects.create(chat=chat, sender=user, content=message)
        model_answer = Message.objects.create(chat=chat, sender=user, content=answer)
        return redirect("chat:ex_chat", chat_name=name)


    return HttpResponse("Failed: No data sent.")
