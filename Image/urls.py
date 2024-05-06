from django.urls import path
from . import views as image_view

urlpatterns = [
    path('', image_view.get_image_upload_page, name='image'),
    path('uploadImage/', image_view.take_image, name='takeImage'),
    path('filterImage/', image_view.filter_image, name='filterImage'),
    path('useCamera/', image_view.use_camera, name="useCamera"),
]
