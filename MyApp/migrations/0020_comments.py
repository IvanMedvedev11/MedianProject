# Generated by Django 5.2 on 2025-05-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0019_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('image', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=20)),
            ],
        ),
    ]
