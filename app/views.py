from collections import defaultdict
from django.conf import settings
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.response import Response

from DjangoVlog.config import config
from .models import Page, PageContent
from .serializers import PageListSerializer, PageDetailSerializer
from .tasks import increment_counters
from .cahce_keys import page_detail_cache_key


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        return PageDetailSerializer if self.action == 'retrieve' else PageListSerializer

    def retrieve(self, request, *args, **kwargs):
        page = self.get_object()
        cache_key = page_detail_cache_key(page.pk)

        cached = cache.get(cache_key)
        if cached:
            data = cached.get('data')
            items_for_counter = cached.get('counter_items', [])
            resp = Response(data)
            if items_for_counter:
                if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                    increment_counters(items_for_counter)
                else:
                    try:
                        increment_counters.delay(items_for_counter)
                    except Exception:
                        increment_counters(items_for_counter)
            return resp

        pcs = (PageContent.objects
               .filter(page=page)
               .select_related('content_type')
               .order_by('position', 'id'))
        ids_by_ct = defaultdict(set)
        for pc in pcs:
            ids_by_ct[pc.content_type_id].add(pc.object_id)

        obj_by_key = {}
        for ct_id, ids in ids_by_ct.items():
            model = ContentType.objects.get_for_id(ct_id).model_class()
            for obj_id, obj in model.objects.in_bulk(ids).items():
                obj_by_key[(ct_id, obj_id)] = obj

        content_objects = []
        items_for_counter = []
        for pc in pcs:
            obj = obj_by_key.get((pc.content_type_id, pc.object_id))
            if obj is None:
                continue
            content_objects.append(obj)
            items_for_counter.append({'ct_id': pc.content_type_id, 'obj_id': pc.object_id})

        serializer = self.get_serializer(page, context={'request': request, 'content_objects': content_objects})
        data = serializer.data

        cache.set(cache_key, {'data': data, 'counter_items': items_for_counter}, timeout=config.page_detail_cache_ttl)

        if items_for_counter:
            if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                increment_counters(items_for_counter)
            else:
                try:
                    increment_counters.delay(items_for_counter)
                except Exception:
                    increment_counters(items_for_counter)

        return Response(data)