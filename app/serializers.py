from rest_framework import serializers
from django.urls import reverse

from .models import Page, Video, Audio


class BaseContentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = None
        fields = ('id', 'type', 'title', 'counter')

    def get_type(self, obj):
        return obj._meta.model_name  # 'video' | 'audio' | future types...


class VideoSerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = Video
        fields = BaseContentSerializer.Meta.fields + ('video_url', 'subtitles_url')


class AudioSerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = Audio
        fields = BaseContentSerializer.Meta.fields + ('transcript',)


CONTENT_SERIALIZER_BY_MODEL = {
    Video: VideoSerializer,
    Audio: AudioSerializer,
}


def serialize_content(obj, context=None):
    Serializer = CONTENT_SERIALIZER_BY_MODEL.get(type(obj))
    if not Serializer:
        return BaseContentSerializer(obj, context=context).data
    return Serializer(obj, context=context).data


class PageListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('id', 'title', 'detail_url')

    def get_detail_url(self, obj):
        request = self.context.get('request')
        url = reverse('api:page-detail', kwargs={'pk': obj.pk})
        return request.build_absolute_uri(url) if request else url


class PageDetailSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('id', 'title', 'contents')

    def get_contents(self, page: Page):
        content_objects = self.context.get('content_objects', [])
        return [serialize_content(obj, context=self.context) for obj in content_objects]