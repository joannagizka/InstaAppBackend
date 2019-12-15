from django.http import HttpResponse
import json
from django.contrib.auth.models import User


def hello(request):
    return HttpResponse('Hello, World! gizka')

def register(request):
    parsed = json.loads(request.body)

    username = parsed['username']
    password = parsed['password']

    #TODO sprawdzic czy uzytkownik o danym username istnieje a jesli istniej to zwrocic odpowiedz
    #zawierajaca informacje o bledzie
    user = User.objects.create_user(username, None, password)

    return HttpResponse('Hello, World user id is: ' + str(user.id))

