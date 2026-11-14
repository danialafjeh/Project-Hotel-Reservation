from django.shortcuts import render, get_object_or_404
from .models import HotelGallery, HotelInfo, HotelRoom
from django.core.cache import cache

# Create your views here.

CACHE_TTL = 60 * 15  # 15 minutes

def home(request):
    sale_rooms = cache.get_or_set(
        'main:home:sale_rooms',
        lambda: list(HotelRoom.objects.filter(is_sale=True)),
        CACHE_TTL
    )

    gallery_images = cache.get_or_set(
        'main:home:gallery',
        lambda: list(HotelGallery.objects.filter(id__in=[1, 2, 3, 8])),
        CACHE_TTL
    )

    info = {
        'gallery': gallery_images,
        'rooms': sale_rooms,
    }

    return render(request, 'home.html', info)


def gallery(request):
    gallery_images = cache.get_or_set(
        'main:gallery:images',
        lambda: list(HotelGallery.objects.all()),
        CACHE_TTL
    )

    info = {'gallery': gallery_images}

    return render(request, 'gallery.html', info)


def about(request):
    hotel_info = cache.get_or_set(
        'main:about:information',
        lambda: get_object_or_404(HotelInfo, id=1),
        CACHE_TTL
    )

    info = {'information': hotel_info}

    return render(request, 'about.html', info)


def rooms(request):
    all_rooms = cache.get_or_set(
        'main:rooms:all',
        lambda: list(HotelRoom.objects.all()),
        CACHE_TTL
    )

    info = {'rooms': all_rooms}

    return render(request, 'rooms.html', info)


