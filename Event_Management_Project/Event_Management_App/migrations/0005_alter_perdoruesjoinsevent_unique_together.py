# Generated by Django 4.2.3 on 2023-07-21 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Event_Management_App', '0004_event_current_capacity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='perdoruesjoinsevent',
            unique_together={('perdorues', 'event')},
        ),
    ]
