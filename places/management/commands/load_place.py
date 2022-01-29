from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place
import requests
import re


class Command(BaseCommand):
    help = 'Load place json data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='*')

    def handle(self, *args, **options):
        for url in options['url']:
            load = load_json(url)
            if load is False:
                self.stdout.write('Место с таким названием и координатами уже создано')


def load_json(url):
    place_json = requests.get(url).json()
    place, is_created = Place.objects.get_or_create(
        title=place_json['title'],
        lng=place_json['coordinates']['lng'],
        lat=place_json['coordinates']['lat'],
        defaults={
            'description_short': place_json['description_short'],
            'description_long': place_json['description_long']
        }
    )
    if not is_created:
        return False
    for image_url in place_json['imgs']:
        image_binary = requests.get(image_url).content
        image_name = re.search(r'\w+.\w+$', image_url).group()
        image, is_created = place.images.get_or_create(
            title=image_name,
            place=place
        )
        if is_created:
            image.image.save(image_name, ContentFile(image_binary), save=True)






