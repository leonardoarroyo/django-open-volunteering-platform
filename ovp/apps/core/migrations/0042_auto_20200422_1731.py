# Generated by Django 2.2.11 on 2020-04-22 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20191121_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresscomponent',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='addresscomponent_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='addresscomponenttype',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='addresscomponenttype_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='availability',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='availability_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='cause',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cause_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='cause',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='uploads.UploadedImage', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='channelcontact',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='channelcontact_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='flair',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='flair_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='flair',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='uploads.UploadedImage', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='googleaddress',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='googleaddress_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='googleregion',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='googleregion_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lead_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='post',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='post',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='gallery.Gallery', verbose_name='gallery'),
        ),
        migrations.AlterField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Post', verbose_name='reply'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='simpleaddress',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='simpleaddress_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='skill_channel', to='channels.Channel'),
        ),
    ]
