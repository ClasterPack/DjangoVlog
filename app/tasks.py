from celery import shared_task
from collections import Counter, defaultdict
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F


@shared_task
def increment_counters(items):
    """
    items: [{'ct_id': int, 'obj_id': int}, ...]
    Инкремент атомарный; одинаковые объекты учитываются кратно.
    """
    grouped = defaultdict(Counter)
    for it in items:
        grouped[it['ct_id']][it['obj_id']] += 1

    for ct_id, obj_counter in grouped.items():
        model = ContentType.objects.get_for_id(ct_id).model_class()
        with transaction.atomic():
            for obj_id, times in obj_counter.items():
                model.objects.filter(pk=obj_id).update(counter=F('counter') + times)