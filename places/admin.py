from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['show_image']
    fields = ('image', 'show_image', 'position')

    def show_image(self, instance):
        multiplier = 200/instance.image.height
        return format_html(
            '<img src="{url}" width="{width}" height={height} />',
            url=instance.image.url,
            width=int(multiplier * instance.image.width),
            height=int(multiplier * instance.image.height)
        )

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
