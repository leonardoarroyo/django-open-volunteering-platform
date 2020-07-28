# Generated by Django 2.2 on 2020-07-28 21:30

from django.db import migrations, models
import uuid

def create_uuid(apps, schema_editor):
    RatingRequest = apps.get_model('ratings', 'RatingRequest')
    for rr in RatingRequest.objects.all():
        rr.permission_token = uuid.uuid4()
        rr.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0014_auto_20200728_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingrequest',
            name='permission_token',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid),
        migrations.AlterField(
            model_name='ratingrequest',
            name='permission_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
