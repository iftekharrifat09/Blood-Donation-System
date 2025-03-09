# Generated by Django 5.1.7 on 2025-03-08 16:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0007_bloodrequest_blood_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodrequest',
            name='accepted',
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='aaccepted_donors',
            field=models.ManyToManyField(blank=True, related_name='accepted_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='accepted_count',
            field=models.IntegerField(default=0),
        ),
    ]
