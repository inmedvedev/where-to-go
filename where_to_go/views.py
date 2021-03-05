from django.http import HttpResponse
from django.template import loader


def show_text(request):
    template = loader.get_template('base.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
