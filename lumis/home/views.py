import os
from django.core.files.base import ContentFile
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core import serializers
from .utils import *
import json
from django.core.files.storage import FileSystemStorage
import urllib.parse


# Необходимо разработать сервис, в котором пользователи
# могут добавлять свои фотографии, смотреть фотографии других,
# отмечать понравившиеся фотографии. Сервис должен состоять из 3
# страниц: страница входа, лента фотографий, страница добавления
# фотографии. Главной страницей является страница входа, другие
# страницы недоступны, пока пользователь не осуществил вход

# •	На странице входа пользователь вводит свое имя и email.
# •	Если пользователь с указанным email’ом не существует,
# то автоматически регистрируется новый пользователь с указанным именем и email’ом
# •	Если пользователь с указанным email’ом существует,
# то осуществляется проверка, ввел ли пользователь то же самое же имя, что и при «регистрации».
# Если имя не совпадает, то должна вывестись ошибка
# •	В обоих случаях на указанный email отправляется ссылка
# для подтверждения входа. Она должна быть случайно генерируемой.
# При переходе по этой ссылке пользователь становится авторизованным

@api_view(['POST'])
def login(request):
    args = ['email', 'name']
    args = {arg: request.POST[arg] for arg in args}
    try:
        user = User.objects.get(email=args['email'])
        link = Link.objects.create(user=user, url=get_random_string(length=100))
        if not user.active:
            send_email(args['email'], urllib.parse.quote('Register'), urllib.parse.quote(link.url))
            return Response({'активация не пройдена'}, status=400)
        if user.name != args['name']:
            return Response({'неправильное имя'}, status=400)
        return Response({'success'}, status=200)
    except User.DoesNotExist:
        user = User.objects.create(email=args['email'], name=args['name'], active=False)
    link = Link.objects.create(user=user, url=get_random_string(length=100))
    send_email(args['email'], urllib.parse.quote('Register'), urllib.parse.quote(link.url))
    return Response({'localhost:8000/{link.url}'}, status=400)


@api_view(['POST'])
def reg(request, rurl):
    try:
        link = Link.objects.get(url=rurl)
        user = link.user
        user.active = True
        user.save()
        return Response({f'Добро пожаловать {user.name}'}, status=200)
    except Link.DoesNotExist:
        return Response({'Ссылка недействительна'}, status=404)


# •	Здесь отображаются выложенные фотографии всех пользователей. Необходимо предусмотреть
# пагинацию (т.е. на первой странице отображаются, например, первые 10 фотографий, на второй – вторые и так далее)
# •	У каждой фотографии указывается число пользователей,
# которые отметили ее понравившейся, а также кнопки для добавления/удаления в/из понравившегося

class infoImage:
    image = "",
    likeCount = 0,

    def to_dict(self):
        data = {}
        data['image'] = self.image
        data['likeCount'] = self.likeCount
        return data

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@api_view(['GET'])
def get_feed(request, page):
    offset = 10
    photos = Photo.objects.order_by('publishedDate')[offset * (page - 1):offset * page]
    resPhotos = []
    for photo in photos:
        image = infoImage()
        # settings.BASE_DIR.__str__() +
        image.image = photo.image.__str__()
        image.likeCount = Like.objects.filter(photo=photo).count()
        resPhotos.append(image.to_dict())
    return Response(json.dumps(resPhotos), status=200)


@api_view(['POST'])
def like(request):
    args = ['photo', 'user']
    args = {arg: request.POST[arg] for arg in args}
    print(args['photo'])
    print(args['user'])
    photo = Photo.objects.get(image=args['photo'])
    user = User.objects.get(email=args['user'])
    Like.objects.create(photo=photo, user=user)
    return Response({'message': 'ok'}, status=200)


# •	Здесь отображается форма добавления фотографии: пользователь должен выбрать изображение
# в формате jpeg. Чтобы убедиться, что загруженный файл – изображение, сервер должен открыть
# его (см. функцию imagecreatefromjpeg) и пересохранить его повторно в формате jpeg (см. функцию imagejpeg).

@api_view(['POST'])
def upload(request):
    # file = request.POST.get('image',    False)

    file = request.FILES['photo']

    full_filename = os.path.join(settings.MEDIA_ROOT, file.name)
    fout = open(full_filename, 'wb+')
    file_content = ContentFile(file.read())
    for chunk in file_content.chunks():
        fout.write(chunk)
    if not Photo.objects.filter(image=file.name).exists():
        photo = Photo.objects.create(image=file.name)
    else:
        photo = Photo.objects.get(image=file.name)
    fout.close()
    path = settings.BASE_DIR.__str__() + photo.image.url
    fout = open(path, 'rb')
    return FileResponse(fout)
    # return HttpResponse(file.read(), content_type='image/jpg')
