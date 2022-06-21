# Generated by Django 3.2.7 on 2022-06-02 13:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialmedia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('1be1e89a-ea97-479d-a967-64f81ec4969c'), primary_key=True, serialize=False)),
                ('post_image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('likes', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
