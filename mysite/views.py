from audioop import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from datetime import datetime
import logging
from django.db import models
from .models import Photo

logger = logging.getLogger(__name__)


def hello(request):
    return HttpResponse('Hello, World! gizka')


def register(request):
    parsed = json.loads(request.body)

    username = parsed['username']
    password = parsed['password']

    if User.objects.filter(username=username).exists():
        return HttpResponseBadRequest('złe dane logowania')

    user = User.objects.create_user(username, None, password)

    return HttpResponse(user.id)


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
        return HttpResponseForbidden('Zle wprowadzone dane!')


@login_required
def my_profile(request):
    user = request.user
    user_photos = Photo.objects.filter(author=user)
    user_photos_parsed = []
    for photo in user_photos:
        user_photos_parsed.append({
            'id': photo.id,
            'description': photo.description
        })
    response = {"username": user.username, 'photos': list(user_photos_parsed)}
    return JsonResponse(response)


@login_required
def add_photo(request):
    up_file = request.FILES['file']
    description = request.POST['description']

    photo = Photo(author=request.user, description=description,
                  created=datetime.now())
    photo.save()

    destination = open('/home/joanna/projekt2020/photos/photo-' + str(photo.id) + "." + up_file.name.split(".")[1],
                       'wb+')
    for chunk in up_file.chunks():
        destination.write(chunk)
    destination.close()

    return JsonResponse({'photoId': photo.id})


def logout_view(request):
    logout(request)
    return redirect('/login')


def get_photo(request, photo_id):
    photo_content = open('/home/joanna/projekt2020/photos/photo-' + str(photo_id) + ".jpg", "rb")
    return HttpResponse(photo_content.read(), content_type="image/jpeg")
