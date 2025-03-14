# Generated by Django 5.1.7 on 2025-03-07 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0002_bloodrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='rejected',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='bloodrequest',
            name='accepted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
