# Generated by Django 4.0.4 on 2022-05-22 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('valence', models.FloatField()),
                ('year', models.IntegerField()),
                ('acousticness', models.FloatField()),
                ('artist', models.CharField(max_length=300)),
                ('danceability', models.FloatField()),
                ('duration', models.IntegerField()),
                ('energy', models.FloatField()),
                ('explicit', models.IntegerField()),
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('instrumentalness', models.FloatField()),
                ('key', models.IntegerField()),
                ('liveness', models.FloatField()),
                ('loudness', models.FloatField()),
                ('mode', models.IntegerField()),
                ('name', models.CharField(max_length=300)),
                ('popularity', models.IntegerField()),
                ('speechiness', models.FloatField()),
                ('tempo', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Song_Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sample')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.song')),
            ],
        ),
    ]
