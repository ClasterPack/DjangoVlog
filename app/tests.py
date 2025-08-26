from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Page, Video, Audio, PageContent


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_pages_list_pagination(self):
        Page.objects.create(title='Page 1')
        Page.objects.create(title='Page 2')

        url = reverse('api:page-list') + '?page=1&page_size=1'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(resp.data['count'], 2)
        self.assertEqual(len(resp.data['results']), 1)
        self.assertIn('detail_url', resp.data['results'][0])

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_page_detail_and_counter_increment(self):
        page = Page.objects.create(title='Page A')
        video = Video.objects.create(title='V1', video_url='https://example.com/v.mp4')
        audio = Audio.objects.create(title='A1', transcript='hello')

        PageContent.objects.create(page=page, content_object=video, position=1)
        PageContent.objects.create(page=page, content_object=audio, position=2)

        url = reverse('api:page-detail', kwargs={'pk': page.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data['contents']), 2)
        self.assertEqual(resp.data['contents'][0]['type'], 'video')
        self.assertEqual(resp.data['contents'][1]['type'], 'audio')

        video.refresh_from_db()
        audio.refresh_from_db()
        self.assertEqual(video.counter, 1)
        self.assertEqual(audio.counter, 1)