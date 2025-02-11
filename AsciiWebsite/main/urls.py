from django.urls import path
from . import views
from .views import home, upload_image, text_to_ascii

urlpatterns = [
#    path("",views.index, name="index"),
    path("", home, name="home"),
    path("image-to-ascii/", upload_image, name="image_to_ascii"),
    path("text-to-ascii/", text_to_ascii, name="text_to_ascii"),





  #  path('', upload_image, name='upload_image'),
   # path('text-to-ascii/', text_to_ascii, name='text_to_ascii'),
]