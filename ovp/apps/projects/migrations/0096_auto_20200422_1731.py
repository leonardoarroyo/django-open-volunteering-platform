# Generated by Django 2.2.11 on 2020-04-22 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0095_auto_20191205_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='apply_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.VolunteerRole', verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='category',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_image', to='uploads.UploadedImage', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='job',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='job',
            name='project',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='jobdate',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobdate_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.GoogleAddress', verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='project',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='project_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='uploads.UploadedImage', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='project',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='items.Item', verbose_name='item'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='organizations.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='projectbookmark',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projectbookmark_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='projectbookmark',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bookmarks', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='projectbookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='volunteerrole',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='volunteerrole_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='volunteerrole',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='roles', to='projects.Project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='work',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='work_channel', to='channels.Channel'),
        ),
        migrations.AlterField(
            model_name='work',
            name='project',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Project'),
        ),
    ]
