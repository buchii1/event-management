# Generated by Django 5.0.6 on 2024-05-17 03:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_booking_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('user', 'event')},
        ),
    ]
