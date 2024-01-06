from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Chat, Message
from .model_answer import answer as ans
from pdf.models import UploadedFile
from .forms import ChooseFileForm
from django.http import HttpResponse


def main(request):
    return render(request, "Ai_reader/main.html")


def chat(request):
    user = request.user
    if request.user.is_authenticated:
        user_files = UploadedFile.objects.filter(user_id=request.user)
        user_chats = Chat.objects.filter(users=user)


        if not user_chats.exists():
            new_chat = Chat.objects.create()
            new_chat.users.add(user)
            new_chat.save()

            chat_replies = []
            return render(
                request,
                "Ai_reader/chat.html",
                {
                    "user_chats": user_chats,
                    "current_chat": new_chat,
                    "chat_replies": chat_replies,
                    "form": ChooseFileForm(),
                },
            )
        else:
            current_chat = user_chats.first()
            chat_replies = Message.objects.filter(chat=current_chat)

            return render(
                request,
                "Ai_reader/chat.html",
                {
                    "user_chats": user_chats,
                    "current_chat": current_chat,
                    "chat_replies": chat_replies,
                    "user_files": user_files,
                },
            )

    else:
        return redirect(reverse("users:eror_aut"))


def ex_chat(request, chat_name):
    user = request.user
    if request.user.is_authenticated:
        user_files = UploadedFile.objects.filter(user_id=request.user)
        user_chats = Chat.objects.filter(users=user)
        x=[]
        for chat in user_chats:
            x.append(chat.name)
        current_chat = user_chats.get(name=chat_name,users_id=user.id)
        chat_replies = Message.objects.filter(chat=current_chat)

        return render(
            request,
            "Ai_reader/chat.html",
            {
                "user_chats": x,
                "current_chat": current_chat,
                "chat_replies": chat_replies,
                'user_files': user_files,
                'form':ChooseFileForm(user=user)
            },
        )
    else:
        return redirect(reverse("users:eror_aut"))



def answer(request):
    if request.method == "POST":
        file = request.POST.get("file")
        user_files = UploadedFile.objects.filter(id=file)

        message = request.POST.get('message')
        answer = ans(user_files[0], message)  
        chat_name = user_files[0].file.name
        name=chat_name.split(".")[0].lower()
        try:
            chat = Chat.objects.get(name=name,users=user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(name=name,users=user)
        chat=Chat.objects.get(name=name,users=user)
        user_message = Message.objects.create(chat=chat, sender=user, content=message)


    return HttpResponse("Failed: No data sent.")
