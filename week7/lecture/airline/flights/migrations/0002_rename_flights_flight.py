# Generated by Django 5.1.4 on 2025-02-04 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Flights',
            new_name='Flight',
        ),
    ]
