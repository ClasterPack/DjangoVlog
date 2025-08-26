import logging

from celery import shared_task
from collections import defaultdict, Counter
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F


@shared_task
def increment_counters(items):
    """
    items: [{'ct_id': <ContentType ID>, 'obj_id': <object ID>}...]
    Повторы НЕ исключаются.
    Один и тот же объект может быть несколько раз на одной странице.
    Значит, counter += количество вхождений.
    """
    grouped = defaultdict(Counter)
    for it in items:
        grouped[it['ct_id']][it['obj_id']] += 1
    for ct_id, obj_counter in grouped.items():
        model = ContentType.objects.get_for_id(ct_id).model_class()
        if model is None:
            continue
        with transaction.atomic():
            for obj_id, count in obj_counter.items():
                logging.info(f"{model.__name__} ID={obj_id} += {count} views")
                updated = model.objects.filter(pk=obj_id).update(counter=F('counter') + count)
                if updated == 0:
                    logging.info(f"{model.__name__} ID={obj_id} not found!")