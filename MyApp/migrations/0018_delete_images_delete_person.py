# Generated by Django 5.2 on 2025-05-11 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0017_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Images',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
