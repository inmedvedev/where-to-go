# Generated by Django 3.1.7 on 2022-01-26 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_image_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='position',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Позиция'),
        ),
    ]
