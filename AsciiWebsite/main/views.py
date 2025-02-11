from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import numpy as np

import pyfiglet
from art import text2art

def home(request):
    return render(request, "main/home.html")


ASCII_CHARS = "@%#*+=-:. 1234567890"

def image_to_ascii(image, width=100):
    img = Image.open(image)
    aspect_ratio = img.height / img.width
    new_height = int(width * aspect_ratio * 0.55)  # Adjust height
    img = img.resize((width, new_height)).convert("L")  # Convert to grayscale

    pixels = np.array(img)
    ascii_art = "\n".join(
        "".join(ASCII_CHARS[p // (255 // (len(ASCII_CHARS) - 1))] for p in row)
        for row in pixels
    )
    return ascii_art

def upload_image(request):
    ascii_output = ""
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            ascii_output = image_to_ascii(image)
    else:
        form = ImageUploadForm()
    
    return render(request, "main/upload.html", {"form": form, "ascii_output": ascii_output})

# List of available fonts for the user to choose from
available_fonts = ["standard", "slant", "block", "banner", "big", "lean", "starwars"]

def text_to_ascii(request):
    ascii_art = ""
    error = None

    if request.method == "POST":
        user_text = request.POST.get("text", "")
        font = request.POST.get("font", "standard")  # Default to "standard" if no font is selected
        width = request.POST.get("width", "80")

        try:
            width = int(width)

            # Generate ASCII text with the selected font
            ascii_art = text2art(user_text, font=font)

            # Resize ASCII using pyfiglet
            figlet_text = pyfiglet.Figlet(font=font, width=width)
            ascii_art = figlet_text.renderText(user_text)

        except Exception as e:
            error = f"Error: {str(e)}"

    return render(
        request, 
        "main/text_to_ascii.html", 
        {"ascii_art": ascii_art, "error": error, "fonts": available_fonts}
    )
