# Generated by Django 5.2 on 2025-05-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0013_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='likes',
            field=models.IntegerField(null=True),
        ),
    ]
