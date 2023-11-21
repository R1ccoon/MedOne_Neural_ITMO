from django.shortcuts import render
from .forms import ImageForm
from PIL import Image


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        print(request.FILES)
        print(request.POST)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Get the current instance object to display in the template
            img_obj = form.instance
            im1 = Image.open(fr"{img_obj.image.url[1:]}")
            im1.save(fr'media/images/{img_obj.title}.png')

            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
        return render(request, 'index.html', {'form': form})
