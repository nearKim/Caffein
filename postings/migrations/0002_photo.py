# Generated by Django 2.0.2 on 2018-03-06 04:30

from django.db import migrations, models
import django.db.models.deletion
import postings.models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=postings.models.get_photo_path, verbose_name='사진')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='postings.Post')),
            ],
        ),
    ]
