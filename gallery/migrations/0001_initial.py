# Generated by Django 2.0 on 2019-02-21 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(unique=True, upload_to='image/seulgi')),
                ('name', models.CharField(default='Seulgi', max_length=24)),
                ('title', models.CharField(max_length=64)),
                ('photo_link', models.CharField(max_length=2048)),
                ('source', models.CharField(max_length=2048)),
                ('views', models.IntegerField(default=0)),
                ('thumbs', models.IntegerField(default=0)),
                ('is_gif', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
