from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline,):
    model = Image
    readonly_fields = ['show_image']
    fields = ('image', 'show_image', 'position')
    extra = 0

    def show_image(self, instance, max_height=200):
        return format_html(
            '<img src="{url}" height="{height}"/>',
            url=instance.image.url,
            height=max_height
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
