import random
import uuid
from typing import List

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from app.models import Page, Video, Audio, PageContent


WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
    "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
    "incididunt", "ut", "labore", "et", "dolore", "magna",
    "aliqua", "enim", "minim", "veniam", "quis", "nostrud"
]


def random_title(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def random_transcript(min_words=10, max_words=60) -> str:
    n = random.randint(min_words, max_words)
    return " ".join(random.choice(WORDS) for _ in range(n))


def random_video_url() -> str:
    return f"https://cdn.example.com/videos/{uuid.uuid4().hex}.mp4"


def random_subtitles_url(prob=0.7):
    return f"https://cdn.example.com/subs/{uuid.uuid4().hex}.vtt" if random.random() < prob else None


class Command(BaseCommand):
    help = "Создает тестовые страницы и контент (видео/аудио) вперемешку с позицией"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--pages", type=int, default=100, help="Сколько страниц создать (default: 100)")
        parser.add_argument("--min-per-page", type=int, default=10, help="Минимум объектов контента на страницу")
        parser.add_argument("--max-per-page", type=int, default=20, help="Максимум объектов контента на страницу")
        parser.add_argument("--seed", type=int, default=None, help="Seed для воспроизводимости (опционально)")

    def handle(self, *args, **options):
        pages_count = options["pages"]
        min_per_page = options["min_per_page"]
        max_per_page = options["max_per_page"]
        seed_value = options.get("seed")

        if seed_value is not None:
            random.seed(seed_value)

        if min_per_page > max_per_page:
            self.stderr.write("min-per-page не может быть больше max-per-page")
            return

        ct_video = ContentType.objects.get_for_model(Video)
        ct_audio = ContentType.objects.get_for_model(Audio)

        created_pages = 0
        created_videos = 0
        created_audios = 0
        created_links = 0

        for i in range(pages_count):
            # Отдельная транзакция на страницу — быстрее и безопаснее
            with transaction.atomic():
                page = Page.objects.create(title=random_title("Page"))

                items_count = random.randint(min_per_page, max_per_page)

                # Сначала решаем порядок типов, чтобы вперемешку
                type_order: List[str] = [random.choice(["video", "audio"]) for _ in range(items_count)]

                videos_to_create: List[Video] = []
                audios_to_create: List[Audio] = []

                for t in type_order:
                    if t == "video":
                        videos_to_create.append(Video(
                            title=random_title("Video"),
                            video_url=random_video_url(),
                            subtitles_url=random_subtitles_url(),
                        ))
                    else:
                        audios_to_create.append(Audio(
                            title=random_title("Audio"),
                            transcript=random_transcript(),
                        ))

                if videos_to_create:
                    Video.objects.bulk_create(videos_to_create, batch_size=1000)
                if audios_to_create:
                    Audio.objects.bulk_create(audios_to_create, batch_size=1000)

                # bulk_create на Postgres проставляет pk в объектах — теперь соберем их в исходном порядке
                v_idx = 0
                a_idx = 0
                ordered_objs = []
                for t in type_order:
                    if t == "video":
                        ordered_objs.append(("video", videos_to_create[v_idx]))
                        v_idx += 1
                    else:
                        ordered_objs.append(("audio", audios_to_create[a_idx]))
                        a_idx += 1

                links_to_create: List[PageContent] = []
                for pos, (t, obj) in enumerate(ordered_objs):
                    if t == "video":
                        links_to_create.append(PageContent(
                            page=page,
                            content_type=ct_video,
                            object_id=obj.pk,
                            position=pos,
                        ))
                    else:
                        links_to_create.append(PageContent(
                            page=page,
                            content_type=ct_audio,
                            object_id=obj.pk,
                            position=pos,
                        ))

                if links_to_create:
                    PageContent.objects.bulk_create(links_to_create, batch_size=1000)

                created_pages += 1
                created_videos += len(videos_to_create)
                created_audios += len(audios_to_create)
                created_links += len(links_to_create)

            if (i + 1) % 10 == 0 or (i + 1) == pages_count:
                self.stdout.write(f"Готово: {i+1}/{pages_count} страниц")

        self.stdout.write(self.style.SUCCESS(
            f"Создано: pages={created_pages}, videos={created_videos}, audios={created_audios}, links={created_links}"
        ))