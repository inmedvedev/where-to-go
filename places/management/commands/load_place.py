from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place
from urllib.parse import urlsplit, unquote
from os import path
from requests.exceptions import HTTPError
import requests


class Command(BaseCommand):
    help = 'Load place json data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='*')

    def handle(self, *args, **options):
        for url in options['url']:
            is_loaded = load_places_to_db(self, url)
            if is_loaded:
                self.stdout.write('Данные загружены')


def load_places_to_db(self, url):
    response = requests.get(url)
    response.raise_for_status()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response.json()['error'])
    place_raw = response.json()
    place, is_created = Place.objects.get_or_create(
        title=place_raw['title'],
        lng=place_raw['coordinates']['lng'],
        lat=place_raw['coordinates']['lat'],
        defaults={
            'description_short': place_raw['description_short'],
            'description_long': place_raw['description_long']
        }
    )
    if not is_created:
        return False
    for image_url in place_raw['imgs']:
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            if 'error' in response:
                raise requests.exceptions.HTTPError(response.json()['error'])
        except HTTPError as error:
            self.stdout.write(
                f'Не удалось загрузить картинку по адресу: {image_url}'
            )
            continue
        image_binary = response.content
        url_path = unquote(urlsplit(image_url).path)
        path_head, image_name = path.split(url_path)
        image = place.images.create(place=place)
        image.image.save(image_name, ContentFile(image_binary), save=True)
    return True
