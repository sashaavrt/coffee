# Generated by Django 4.2.18 on 2025-05-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0006_reportarchive'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodel',
            name='quality',
            field=models.FloatField(default=0),
        ),
    ]
