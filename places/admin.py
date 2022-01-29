from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline,):
    model = Image
    readonly_fields = ['show_image']
    fields = ('image', 'show_image', 'position')
    extra = 0

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
