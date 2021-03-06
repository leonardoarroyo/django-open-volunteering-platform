# Generated by Django 2.2.11 on 2020-04-22 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0059_auto_20190815_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverificationtoken',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='emailverificationtoken_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='emailverificationtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='passwordhistory',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='passwordhistory_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='passwordhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='passwordrecoverytoken',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='passwordrecoverytoken_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='passwordrecoverytoken',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='avatar_user', to='uploads.UploadedImage', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.OneToOneField(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.GoogleAddress', verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='userprofile_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_userprofile_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
