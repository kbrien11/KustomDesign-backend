from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token




urlpatterns = [
    path('register',views.createUser),
    path('uploadImage/<user_pk>',views.upload_image),
    path('login',views.login),
    path('images',views.get_images),
    path('addLikeToImage/<artist_id>/<image_id>',views.addLike),
    path('images/<user_pk>',views.imagesPerUser),
    path('deleteImage/<user_pk>/<id>',views.deletePicture),
    path('artists/<artist_ids>',views.get_artists),
    path('addMatch/<user>/<artist>/<picture>',views.addMatch),
    path('imagePerArtist/<artist_id>/<username>',views.imagePerArtist),
    path('artistProfilePiceture/<artist_id>/<artist_username>',views.artist_profile_picture)
]

