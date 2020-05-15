# Generated by Django 3.0.6 on 2020-05-13 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Group', '0004_channel'),
        ('Post', '0003_post_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Post.Post')),
                ('parentchannel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_channel', to='Group.Channel')),
            ],
            bases=('Post.post',),
        ),
    ]
