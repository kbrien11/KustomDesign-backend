from operator import mod
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Picture, CustomUser, MatchRelationship


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ["id", "image", "user_pk", "size", "artist_id", "match", "price"]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "password",
            "email",
            "date_joined",
            "user_type",
            "first_name",
            "last_name",
            "username",
            "profile_image",
        ]


class MatchRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRelationship
        fields = ["id", "user_pk", "artist", "picture_pk"]
