# Generated by Django 2.0.3 on 2018-04-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20180406_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='latest_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
