# Generated by Django 3.1.7 on 2022-01-26 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_remove_place_json_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='position',
            field=models.PositiveIntegerField(null=True, unique=True, verbose_name='Позиция'),
        ),
    ]
