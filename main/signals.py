from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import HotelRoom, HotelGallery, HotelInfo



@receiver([post_save, post_delete], sender=HotelRoom)
def invalidate_room_cache(sender, **kwargs):
    cache.delete_many([
        'main:home:sale_rooms',
        'main:rooms:all',
    ])


@receiver([post_save, post_delete], sender=HotelGallery)
def invalidate_gallery_cache(sender, **kwargs):
    cache.delete_many([
        'main:home:gallery',
        'main:gallery:images',
    ])


@receiver([post_save, post_delete], sender=HotelInfo)
def invalidate_hotel_info_cache(sender, **kwargs):
    cache.delete('main:about:information')