from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType

from .models import PageContent, Video, Audio
from .cahce_keys import page_detail_cache_key


@receiver(post_save, sender=PageContent)
@receiver(post_delete, sender=PageContent)
def invalidate_page_detail_on_link_change(sender, instance: PageContent, **kwargs):
    cache.delete(page_detail_cache_key(instance.page_id))


def _invalidate_pages_for_content(instance):
    ct = ContentType.objects.get_for_model(type(instance))
    page_ids = (PageContent.objects
                .filter(content_type=ct, object_id=instance.pk)
                .values_list('page_id', flat=True)
                .distinct())
    for pid in page_ids:
        cache.delete(page_detail_cache_key(pid))


@receiver(post_save, sender=Video)
@receiver(post_delete, sender=Video)
def invalidate_on_video_change(sender, instance: Video, **kwargs):
    _invalidate_pages_for_content(instance)


@receiver(post_save, sender=Audio)
@receiver(post_delete, sender=Audio)
def invalidate_on_audio_change(sender, instance: Audio, **kwargs):
    _invalidate_pages_for_content(instance)