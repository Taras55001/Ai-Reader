from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Chat, Message
from .dolly_answer import answer as ans



def main(request):
    return render(request, "Ai_reader/main.html")


def chat(request):
    user = request.user
    if request.user.is_authenticated:
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
                },
            )
    else:
        return redirect(reverse("users:eror_aut"))


def answer(request):

    ans('chat\media\uploads\PlayerGuide.pdf', 'How many players in the game?')

    return render(request, "Ai_reader/chat.html")
