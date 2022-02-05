from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place
from urllib.parse import urlsplit, unquote
from os import path
from requests.exceptions import HTTPError, ConnectionError
import requests


class Command(BaseCommand):
    help = 'Load place json data'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='*')

    def handle(self, *args, **options):
        for url in options['url']:
            response = get_response(self, url)
            is_loaded = load_places_to_db(self, response)
            if is_loaded:
                self.stdout.write('Данные загружены')


def get_response(self, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if 'error' in response:
            raise requests.exceptions.HTTPError(response.json()['error'])
    except (HTTPError, ConnectionError) as error:
        self.stdout.write(str(error))
        return None
    return response


def load_places_to_db(self, response):
    if response is None:
        return False
    place_json = response.json()
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
        response = get_response(self, image_url)
        if response is None:
            continue
        image_binary = response.content
        url_path = unquote(urlsplit(image_url).path)
        path_head, image_name = path.split(url_path)
        image = place.images.create(place=place)
        image.image.save(image_name, ContentFile(image_binary), save=True)
    return True
