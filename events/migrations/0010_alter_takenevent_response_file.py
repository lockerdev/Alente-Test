# Generated by Django 3.2.4 on 2021-06-24 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_takenevent_response_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takenevent',
            name='response_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
