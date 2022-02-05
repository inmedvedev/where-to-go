from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание',
                                         blank=True,
                                         null=True)
    description_long = HTMLField('Описание', blank=True, null=True)
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['title', 'lng', 'lat']


class Image(models.Model):
    place = models.ForeignKey('Place',
                              on_delete=models.CASCADE,
                              verbose_name='Место',
                              related_name='images')
    image = models.ImageField('Картинка')
    position = models.PositiveSmallIntegerField('Позиция',
                                                default=0,
                                                blank=True)

    def __str__(self):
        return f'{self.image}'

    class Meta:
        unique_together = ['place', 'image']
        ordering = ('position',)
