# Generated by Django 5.0.6 on 2024-05-16 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_event_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizers',
            field=models.ManyToManyField(related_name='organizers', to='main.organizer'),
        ),
    ]
