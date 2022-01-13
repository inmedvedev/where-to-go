from django.http import HttpResponse
from django.shortcuts import render
from places.models import Place, Image

DEFAULT_IMAGE_URL = ['/home/ivan/where-to-go/media/default.jpg']

def show_places(request):
    place_json = {
        "type": "FeatureCollection",
        "features": []
    }
    places = Place.objects.all()
    for place in places:
        print(str(place.json_path))
        place_json["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "detailsUrl": str(place.json_path)
            }
        },
        )

    return render(request, 'index.html', context={'place_json': place_json})
