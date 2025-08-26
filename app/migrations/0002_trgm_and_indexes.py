from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension
from django.contrib.postgres.indexes import GinIndex


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddIndex(
            model_name='page',
            index=GinIndex(fields=['title'], name='page_title_trgm', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='video',
            index=GinIndex(fields=['title'], name='video_title_trgm', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='audio',
            index=GinIndex(fields=['title'], name='audio_title_trgm', opclasses=['gin_trgm_ops']),
        ),
    ]