# Generated by Django 3.0.3 on 2020-05-17 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0005_poll_pollchoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollchoice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_choice', to='Post.Post'),
        ),
    ]