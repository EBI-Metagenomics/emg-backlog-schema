# Generated by Django 2.0.3 on 2018-05-29 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0022_auto_20180410_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='assembly',
            name='ena_last_update',
            field=models.DateField(null=True),
        ),
    ]
