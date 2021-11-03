from django.shortcuts import render, HttpResponseRedirect

from .models import VoteButton, Message
from django.db.models import F
from datetime import datetime


def home(request):
    buttons = VoteButton.objects.all()
    messages = Message.objects.order_by('-pk')[:5]
    return render(request, 'home/home.html', {'buttons': buttons, 'messages': messages})


def increase_counter(request, pk):
    vote_btn = VoteButton.objects.filter(pk=pk)
    print(vote_btn[0])
    message = Message(message=f'{vote_btn[0]} Sent by {request.user.username} at {datetime.now().strftime("%H:%M")}',
                      btn=vote_btn[0])
    vote_btn = vote_btn.update(count=F('count') + 1)
    message.save()
    return HttpResponseRedirect("/")


def message_details(request, pk):
    message = Message.objects.get(pk=pk)
    return render(request, 'home/message.html', {'message': message})

