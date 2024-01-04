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
                    'form':ChooseFileForm()
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
                    'user_files': user_files
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
        file_path = 'chat/media/uploads/PlayerGuide.pdf' 
        answer = ans(user_files[0], message)  

        chat_name = user_files[0].file.name  
        print(Chat.objects.filter(name=chat_name))
        if Chat.objects.filter(name=chat_name) == None:
            chat = Chat.objects.create(name=chat_name)

        user_message = Message.objects.create(chat=chat, sender=user, content=message)

        # Створення повідомлення від бота (ваша логіка генерації відповіді)
        bot_message_content = "Це відповідь бота на ваше повідомлення."
        bot_message = Message.objects.create(chat=chat, sender=user, content=bot_message_content)
        


        return HttpResponse("Success: Data sent to 'ans' function.")
    
    return HttpResponse("Failed: No data sent.")
