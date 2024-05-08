from django.shortcuts import render, redirect
from Image.models import Image
from django.http import HttpRequest, HttpResponse
from django.template import TemplateDoesNotExist

# Create your views here.


def get_image_upload_page(request: HttpRequest) -> HttpResponse:
    """
    Renders the image upload page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered image upload page.
    """
    try:
        # Attempt to render the image upload page
        return render(request, 'Image/ImageUpload.html')

    except TemplateDoesNotExist:
        # Handle case where the specified template do`es not exist
        return HttpResponse("Error: The requested template does not exist.", status=404)

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)


def take_image(request: HttpRequest) -> HttpResponse:
    """
    Renders the camera capture page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered camera capture page.
    """
    try:
        if request.method == "GET":
            # Render the initial page where users can capture or upload an image
            return render(request, 'Image/Upload.html')
        else:
            # Process the uploaded image file
            image = request.FILES['emo-image']
            emo_image = Image(user=request.user, Image_url=image)
            emo_image.save()
            return redirect('filterImage')

    except KeyError:
        # Handle case where the image key is not found in the uploaded files
        return HttpResponse("No image was uploaded. Please try again.", status=400)

    except Exception as e:
        # General catch-all for any other unexpected exceptions
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)


def use_camera(request: HttpRequest) -> HttpResponse:
    try:
        if request.method == "GET":
            # Render the camera capture page
            return render(request, 'Image/CaptureImage.html')
        else:
            # Redirect to the next step after capturing the image
            return redirect('filterImage')

    except Exception as e:
        # General catch-all for any unexpected errors
        return HttpResponse(f"An unexpected error occurred: {e}", status=500)


def filter_image(request: HttpRequest) -> HttpResponse:
    """
    Redirects to the 'emotion' view.

    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Redirects to the 'emotion' view.
    """
    try:
        # Attempt to redirect to the 'emotion' view
        return redirect('emotion')
    except Exception as e:
        # General catch-all for any unexpected errors that might occur during redirection
        return HttpResponse(f"An unexpected error occurred during redirection: {e}", status=500)


