from django.db import models
from django.conf import settings


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = models.TextField('Описание')
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')
    json_path = models.FilePathField('Адрес json файла', path=settings.PLACES_FILE_DIR, default='')

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    place = models.ForeignKey('Place',
                              on_delete=models.CASCADE,
                              verbose_name='Место',
                              related_name='images')
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка')

    def __str__(self):
        return f'{self.title}'
