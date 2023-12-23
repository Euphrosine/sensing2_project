# Generated by Django 4.2.6 on 2023-12-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.FloatField(null=True)),
                ('current1', models.FloatField(null=True)),
                ('current2', models.FloatField(null=True)),
                ('current3', models.FloatField(null=True)),
                ('vibration', models.FloatField(null=True)),
                ('speed', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MachineLearningPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('prediction', models.FloatField()),
            ],
        ),
    ]
