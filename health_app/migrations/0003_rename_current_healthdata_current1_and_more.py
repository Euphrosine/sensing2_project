# Generated by Django 4.2.6 on 2023-11-03 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0002_rename_bim_healthdata_current_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthdata',
            old_name='current',
            new_name='current1',
        ),
        migrations.AddField(
            model_name='healthdata',
            name='current2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='healthdata',
            name='current3',
            field=models.FloatField(null=True),
        ),
    ]