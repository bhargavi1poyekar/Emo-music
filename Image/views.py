from django.shortcuts import render, redirect
from Image.models import Image
from django.http import HttpRequest, HttpResponse

# Create your views here.


def get_image_upload_page(request: HttpRequest) -> HttpResponse:
    """
    Renders the image upload page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered image upload page.
    """
    return render(request, 'Image/ImageUpload.html')


def take_image(request: HttpRequest) -> HttpResponse:
    """
    Renders the camera capture page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered camera capture page.
    """
    if request.method == "GET":
        return render(request, 'Image/Upload.html')
    else:
        image = request.FILES['emo-image']
        emo_image = Image(user=request.user, Image_url=image)
        emo_image.save()
        return redirect('filterImage')


def use_camera(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'Image/CaptureImage.html')
    else:
        return redirect('filterImage')


def filter_image(request: HttpRequest) -> HttpResponse:
    """
    Redirects to the 'emotion' view.

    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Redirects to the 'emotion' view.
    """
    return redirect('emotion')
