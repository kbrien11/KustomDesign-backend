import email
from hashlib import new
import numbers
from django.shortcuts import render
from requests import request


from .models import CustomUser, Picture, MatchRelationship
from .serializers import (
    CustomUserSerializer,
    PictureSerializer,
    MatchRelationshipSerializer,
)
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.views import Response

# Create your views here.


@api_view(["POST"])
def createUser(request):
    print(request.data)
    first_name = request.data["first_name"]
    last_name = request.data["last_name"]
    username = request.data["username"]
    profile_image = request.data["profile_image"]
    location = request.data["location"]

    pass_hash = make_password(request.data["password"])
    print(pass_hash)
    new_user = CustomUser(
        email=request.data["email"],
        password=pass_hash,
        user_type=request.data["user_type"],
        first_name=first_name,
        last_name=last_name,
        username=username,
        profile_image=profile_image,
        location=location,
    )
    if new_user:
        new_user.save()
        user = CustomUser.objects.filter(email=request.data["email"]).first()
        print(user)

        return Response({"type": user.user_type})
    else:
        return Response({"error": "errro"})


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user_obj = CustomUser.objects.filter(email__iexact=email).first()
    ser = CustomUserSerializer(user_obj, many=False)
    print(user_obj)
    if user_obj:
        validate_password = check_password(password, ser.data["password"])
        print(validate_password, password)
        if validate_password:
            return Response(
                {
                    "user_type": ser.data["user_type"],
                    "id": ser.data["id"],
                    "profile_image": ser.data["profile_image"],
                }
            )
        else:
            print("error logging in")
            return Response({"Error": "invalid password"})
    else:
        print("email is wrong")
        return Response({"Error": "invalid email"})


@api_view(["POST"])
def upload_image(request, user_pk):
    user = CustomUser.objects.filter(id=user_pk).first()
    user_ser = CustomUserSerializer(user, many=False)
    print(user_ser.data)
    if user_ser:
        new_picture = Picture(
            user_pk=user_pk,
            image=request.data["image"],
            size=request.data["size"],
            price=request.data["price"],
        )
        if new_picture:
            new_picture.save()
            return Response({"user": user_ser.data})
        return Response({"error": "error with uploading image"})
    else:
        return Response({"error": "invalid user"})


@api_view(["GET"])
def get_images(request):
    images = Picture.objects.filter(match=0).all()
    picture_ser = PictureSerializer(images, many=True)
    if picture_ser:
        return Response({"images": picture_ser.data, "showDetails": True})
    else:
        return Response({"error": "invalid user"})


@api_view(["GET"])
def home_images(request):
    images = Picture.objects.all()
    picture_ser = PictureSerializer(images, many=True)
    if picture_ser:
        return Response({"images": picture_ser.data, "showDetails": True})
    else:
        return Response({"error": "invalid user"})


@api_view(["POST"])
def addLike(request, artist_id, image_id):
    picture = Picture.objects.filter(id=image_id).first()
    picture_ser = PictureSerializer(picture, many=False)
    if picture_ser:
        if artist_id in picture.artist_id:
            return Response({"error": "artist already added "})
        picture.artist_id.append(artist_id)
        picture.save(update_fields=["artist_id"])
        return Response({"data": picture_ser.data["artist_id"]})
    else:
        return Response({"error": "invalid image"})


@api_view(["GET"])
def imagesPerUser(Request, user_pk):
    print(user_pk)
    image_data = []
    images = Picture.objects.filter(user_pk=user_pk).all()
    print(images)
    images_ser = PictureSerializer(images, many=True)
    if images_ser:
        for image in images_ser.data:
            print(image)
            if image["match"] == 0:
                image_data.append(image)
            else:
                continue
        return Response({"images": image_data, "showDetails": True})
    else:
        return Response({"error": "invalid user"})


@api_view(["DELETE"])
def deletePicture(request, user_pk, id):
    picture = Picture.objects.filter(id=id, user_pk=user_pk).first()
    print(picture)
    if picture:
        picture.delete()

        return Response({"data": id})
    else:
        return Response({"error": "invalid user"})


@api_view(["GET"])
def get_artists(request, artist_ids):
    artist_list = list(artist_ids.split(","))
    print(artist_list)
    usernames = []
    for i in artist_list:
        artist = CustomUser.objects.filter(id=i).first()
        artist_ser = CustomUserSerializer(artist, many=False)
        if artist_ser:
            print(artist_ser.data)
            usernames.append(artist_ser.data["username"])

    return Response({"data": usernames})


@api_view(["GET"])
def addMatch(request, artist, user, picture):
    image = Picture.objects.filter(id=picture).first()
    artist_username = CustomUser.objects.filter(username=artist).first()
    if image:
        image.match = 1
        image.artist_username = artist
        artist_username.artist_picture_list.append(image.image)
        artist_username.save(update_fields="artist_picture_list")
        image.save(update_fields=["match", "artist_username"])
        new_match = MatchRelationship(user_pk=user, artist=artist, picture_pk=image)
        if new_match:
            new_match.save()

        return Response({"match added": "success"})
    else:
        return Response({"error": "couldnt add match"})


@api_view(["GET"])
def imagePerArtist(request, artist_id, username):
    picture_list = []
    print(artist_id)
    if artist_id != "null":
        artist = CustomUser.objects.filter(id=artist_id).first()
        artist_username = artist.username
    else:
        artist_username = username
    if artist_username:
        artistMatches = MatchRelationship.objects.filter(artist=artist_username).all()
        artistMatchesSer = MatchRelationshipSerializer(artistMatches, many=True)
        if artistMatchesSer:
            for match in artistMatchesSer.data:
                picture_pk = match["picture_pk"]

                image = Picture.objects.filter(id=picture_pk).first()
                image_ser = PictureSerializer(image, many=False)
                picture_list.append(image_ser.data)

            return Response({"images": picture_list, "showDetails": False})
        else:
            return Response({"data": "error"})


@api_view(["GET"])
def totalArtistsImages(request):
    artists = CustomUser.objects.filter(user_type="Artist").all()
    artist_ser = CustomUserSerializer(artists, many=True)
    images_list = []
    print(artist_ser)
    for artist in artist_ser.data:
        print(artist)
        if len(artist["artist_picture_list"]) > 0:
            images_list.append(artist)
        else:
            continue
    return Response({"images": images_list})


@api_view(["GET"])
def artist_profile_picture(reqest, artist_id, artist_username):
    print(artist_id)
    if artist_id != "null":
        artist = CustomUser.objects.filter(id=artist_id).first()
        artist_name = artist.username
    else:
        artist_name = artist_username
    if artist_name:
        artist = CustomUser.objects.filter(username=artist_name).first()
        artist_ser = CustomUserSerializer(artist, many=False)
        if artist_ser.data:
            return Response(
                {
                    "data": artist_ser.data["profile_image"],
                    "first_name": artist_ser.data["first_name"],
                    "last_name": artist_ser.data["last_name"],
                }
            )
        else:
            return Response({"data": "error"})
