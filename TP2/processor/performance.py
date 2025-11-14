import requests
from PIL import Image
from io import BytesIO
import base64


def process_images(request):
    image_urls = request.get("image_urls")
    if not image_urls or not isinstance(image_urls, list):
        return {"error": "No se proporcionó una lista válida de URLs de imágenes"}

    thumbnails = []
    for url in image_urls:
        try:
            # Descargar imagen
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))

            # Crear thumbnail
            img.thumbnail((100, 100))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            thumbnail_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            thumbnails.append({"url": url, "thumbnail": thumbnail_base64})
        except Exception as e:
            thumbnails.append({"url": url, "error": str(e)})

    return {"thumbnails": thumbnails}