# Generated by Django 5.1.7 on 2025-03-09 05:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0011_remove_bloodrequest_rejected_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='request_ignored_by_donors',
            field=models.ManyToManyField(blank=True, related_name='ignored_donors', to=settings.AUTH_USER_MODEL),
        ),
    ]
