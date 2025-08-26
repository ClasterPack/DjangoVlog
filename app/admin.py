from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import Page, PageContent, Video, Audio


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'counter', 'video_url')
    list_display_links = ('id', 'title')
    search_fields = ('title__istartswith',)
    readonly_fields = ('counter',)
    fields = ('title', 'video_url', 'subtitles_url', 'counter')


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'counter')
    list_display_links = ('id', 'title')
    search_fields = ('title__istartswith',)
    readonly_fields = ('counter',)
    fields = ('title', 'transcript', 'counter')


class PageContentInline(admin.TabularInline):
    model = PageContent
    extra = 1
    fields = ('position', 'content_type', 'object_id', 'content_counter', 'content_object_preview')
    readonly_fields = ('content_object_preview', 'content_counter')
    ordering = ('position',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'content_type':
            allowed = ContentType.objects.get_for_models(Video, Audio).values()
            kwargs['queryset'] = ContentType.objects.filter(id__in=[ct.id for ct in allowed])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def content_object_preview(self, obj):
        content_type = obj.content_type.name if obj.content_type else '-'
        label = str(obj.content_object) if obj and obj.content_object else '-'
        return f'{content_type}: {label}'

    def content_counter(self, obj):
        if obj and obj.content_object:
            return obj.content_object.counter
        return '-'
    content_counter.short_description = 'views'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title__istartswith',)
    inlines = [PageContentInline]