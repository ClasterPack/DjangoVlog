from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.operations import TrigramExtension
from django.contrib.postgres.indexes import GinIndex


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]
    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('counter', models.PositiveIntegerField(default=0)),
                ('transcript', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('counter', models.PositiveIntegerField(default=0)),
                ('video_url', models.URLField()),
                ('subtitles_url', models.URLField(blank=True, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('position', models.PositiveIntegerField(default=0)),
                ('content_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='contenttypes.ContentType'
                )),
                ('page', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='page_contents',
                    to='app.Page'
                )),
            ],
            options={
                'ordering': ['position', 'id'],
            },
        ),
        migrations.AddConstraint(
            model_name='pagecontent',
            constraint=models.UniqueConstraint(
                fields=('page', 'content_type', 'object_id'),
                name='uniq_page_content_object'
            ),
        ),
        migrations.AddConstraint(
            model_name='pagecontent',
            constraint=models.UniqueConstraint(fields=('page', 'position'), name='uniq_page_position_per_page'),
        ),
        migrations.AddIndex(
            model_name='page',
            index=GinIndex(
                fields=['title'],
                name='page_title_trgm',
                opclasses=['gin_trgm_ops'],
            ),
        ),
        migrations.AddIndex(
            model_name='video',
            index=GinIndex(
                fields=['title'],
                name='video_title_trgm',
                opclasses=['gin_trgm_ops'],
            ),
        ),
        migrations.AddIndex(
            model_name='audio',
            index=GinIndex(
                fields=['title'],
                name='audio_title_trgm',
                opclasses=['gin_trgm_ops'],
            ),
        ),
        migrations.AddIndex(
            model_name='pagecontent',
            index=models.Index(
                fields=['page', 'position'],
                name='app_pagecon_page_pos_idx'
            ),
        ),
    ]