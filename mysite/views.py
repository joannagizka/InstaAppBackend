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
from django.db import models, IntegrityError
from .models import Photo, Observation, Comment
from django.shortcuts import get_object_or_404

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


@login_required
def get_photo_meta(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    comments = Comment.objects.filter(photo=photo).all()

    comments_parsed = []
    for comment in comments:
        comments_parsed.append({
            'authorId': comment.author.id,
            'authorUsername': comment.author.username,
            'creationTime': comment.created,
            'content': comment.content,
            'isMe': request.user == comment.author
        })

    return JsonResponse({
        'description': photo.description,
        'creationTime': photo.created,
        'authorId': photo.author.id,
        'authorUsername': photo.author.username,
        'isMe': request.user == photo.author,
        'comments': list(comments_parsed)
    })


@login_required
def all_photos(request):
    photos = Photo.objects.all()

    observations = Observation.objects.filter(follower=request.user).all()
    observed_users = set()
    for observation in observations:
        observed_users.add(observation.following)

    photos_parsed = []
    for photo in photos:
        if photo.author in observed_users or photo.author == request.user:
            photos_parsed.append({
                'id': photo.id,
                'description': photo.description
            })

    response = {'photos': list(photos_parsed)}
    return JsonResponse(response)


@login_required
def get_users(request):
    user = request.user
    other_users = User.objects.exclude(id=user.id).exclude(id=1).all()
    observations = Observation.objects.filter(follower=user).all()
    observed_users = set()
    for observation in observations:
        observed_users.add(observation.following)

    users_parsed = []
    for other_user in other_users:
        users_parsed.append({
            'id': other_user.id,
            'username': other_user.username,
            'isObserved': other_user in observed_users,
        })

    return JsonResponse({'users': list(users_parsed)})

@login_required
def follow(request, other_user_id):
    try:
        other_user = get_object_or_404(User, pk=other_user_id)
        observation = Observation(follower=request.user, following=other_user)
        observation.save()
    except IntegrityError:
        pass
    return HttpResponse()

@login_required
def unfollow(request, other_user_id):
    other_user = get_object_or_404(User, pk=other_user_id)
    Observation.objects.filter(follower=request.user, following=other_user).delete()
    return HttpResponse()


@login_required
def add_comment(request, photo_id):
    parsed = json.loads(request.body)
    content = parsed['content']

    photo = get_object_or_404(Photo, pk=photo_id)

    comment = Comment(photo=photo, author=request.user, content=content, created=datetime.now())
    comment.save()
    return get_photo_meta(request, photo_id)