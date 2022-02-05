from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from places.models import Place
from django.urls import reverse


def show_places(request):
    place_features = {
        "type": "FeatureCollection",
        "features": []
    }
    places = Place.objects.all()
    for place in places:
        place_features["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "detailsUrl": reverse('place-detail', args=[place.id])
            }
        },
        )

    return render(
                    request, 'index.html',
                    context={'place_features': place_features}
    )


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    place_images = place.images.all()
    image_urls = [place_image.image.url for place_image in place_images]
    response = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
        }
    }
    return JsonResponse(response,
                        safe=False,
                        json_dumps_params={'ensure_ascii': False,
                                           'indent': 4}
                        )
