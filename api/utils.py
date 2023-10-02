from django.conf import settings

def get_image_with_host(image_url):
    if settings.DEBUG:
        host = settings.HOST
        return f"{host}{image_url}"
    else:
        return f"{image_url}"
