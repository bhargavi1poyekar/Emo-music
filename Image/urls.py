from django.urls import path,include
from . import views as image_view

urlpatterns = [
    path('',image_view.image, name='image'),
    path('uploadImage/',image_view.takeImage, name='takeImage'),
    path('filterImage/',image_view.filterImage, name='filterImage'),
    # path('useCamera/',image_view.useCamera,name="useCamera"),
]