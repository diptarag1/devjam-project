# Generated by Django 3.0.3 on 2020-05-19 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Group', '0008_group_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='link',
            field=models.URLField(blank=True),
        ),
    ]
