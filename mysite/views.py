from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def hello(request):
    return HttpResponse('Hello, World! gizka')


def register(request):
    parsed = json.loads(request.body)

    username = parsed['username']
    password = parsed['password']

    if User.objects.filter(username=username).exists():
        return HttpResponseBadRequest('zle')

    user = User.objects.create_user(username, None, password)

    return HttpResponse('Hello, World user id is: ' + str(user.id))


def logging(request):
    parsed = json.loads(request.body)

    userData = parsed['user']
    username = userData['username']
    password = userData['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('zalogowano')
    else:
        return HttpResponse('Zle wprowadzone dane!')

