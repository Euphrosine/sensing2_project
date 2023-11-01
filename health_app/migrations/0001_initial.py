# Generated by Django 4.2.6 on 2023-10-26 11:41

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
                ('bim', models.FloatField(null=True)),
                ('temperature', models.FloatField(null=True)),
                ('spo2', models.FloatField(null=True)),
                ('strick', models.FloatField(null=True)),
                ('bp', models.FloatField(null=True)),
            ],
        ),
    ]