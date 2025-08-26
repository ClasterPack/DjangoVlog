from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"),auto_now=True)

    class Meta:
        abstract = True


class ContentBase(TimeStampedModel):
    title = models.CharField(_("Title"),max_length=255)
    counter = models.PositiveIntegerField(_("Views"),default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Video(ContentBase):
    video_url = models.URLField(_("Video URL"))
    subtitles_url = models.URLField(_("Subtitles URL"),blank=True, null=True)


class Audio(ContentBase):
    transcript = models.TextField(_("Description"),blank=True)


class Page(TimeStampedModel):
    title = models.CharField(_("Title"),max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class PageContent(TimeStampedModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_contents', verbose_name=_("Page"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"))
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    position = models.PositiveIntegerField(verbose_name=_("Position"), default=0)

    class Meta:
        ordering = ['position', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['page', 'content_type', 'object_id'],
                name='uniq_page_content_object'
            ),
            models.UniqueConstraint(
                fields=['page', 'position'],
                name='uniq_page_position_per_page'
            ),
        ]

        indexes = [
            models.Index(fields=['page', 'position']),
        ]

    def __str__(self):
        return f'{self.page} -> {self.content_type}#{self.object_id} (pos {self.position})'

    def clean(self):
        if PageContent.objects.filter(page=self.page, position=self.position).exclude(pk=self.pk).exists():
            raise ValidationError(_("Position already bind."))

        if PageContent.objects.filter(page=self.page, content_type=self.content_type, object_id=self.object_id).exclude(
                pk=self.pk).exists():
            raise ValidationError(_("Content already exists."))