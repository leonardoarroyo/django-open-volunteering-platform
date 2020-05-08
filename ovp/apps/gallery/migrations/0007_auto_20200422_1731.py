# Generated by Django 2.2.11 on 2020-04-22 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20190314_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gallery_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]