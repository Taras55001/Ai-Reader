from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Chat, Message
from .dolly_answer import answer as ans
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
        x=[]
        for chat in user_chats:
            print(chat.name)
            x.append(chat.name)
        return render(
            request,
            "Ai_reader/chat.html",
            {
                "user_chats": x,
                'user_files': user_files,
                'form':ChooseFileForm(user=user)
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
    if request.method == 'POST':
        user = request.user
        file = request.POST.get('file')
        user_files = UploadedFile.objects.filter(id=file)

        message = request.POST.get('message')
        file_extension = file.name.split(".")[-1].lower()
        answer = ans(user_files[0], message)  
        print(answer)
        chat_name = user_files[0].file.name  
        try:
            chat = Chat.objects.get(name=chat_name,users=user)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(name=chat_name,users=user)
        chat=Chat.objects.get(name=chat_name,users=user)
        user_message = Message.objects.create(chat=chat, sender=user, content=message)


        bot_message = Message.objects.create(chat=chat, sender=user, content=answer)
        
        return redirect(to='chat:ex_chat', chat_name=chat_name)
    
    return HttpResponse("Failed: No data sent.")
