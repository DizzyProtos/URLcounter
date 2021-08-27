from django.http import HttpResponse
from urlcounter.url_counter_service import start_url_counter
from django.db.models import ObjectDoesNotExist
from .models import url_model
import json
import re


def add_url(request):
    body_args = json.loads(request.body)

    validate_url_regex = regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not validate_url_regex.match(body_args['url']):
        return HttpResponse('URL is not valid, please provide correct URL')

    existing_id = url_model.get_existing_id(body_args['url'])
    if existing_id is None:
        new_model = url_model(url=body_args['url'], counted_json='')
        new_model.save()
        start_url_counter(new_model.url, new_model.id)
        return HttpResponse(new_model.id)
    else:
        return HttpResponse(existing_id)


def update_url(request, url_id):
    try:
        existing_model = url_model.objects.get(id=url_id)
        existing_model.counted_json = ''
    except ObjectDoesNotExist:
        return HttpResponse(f"URL with id {url_id} doesn't exist")
    existing_model.save()
    start_url_counter(existing_model.url, existing_model.id)
    return HttpResponse(existing_model.id)


def get_result(request, url_id):
    try:
        handled_model = url_model.objects.get(id=url_id)
    except ObjectDoesNotExist:
        return HttpResponse(f"URL with id {url_id} doesn't exist")

    if handled_model.counted_json == '':
        return HttpResponse("URL processing isn't finished")
    elif handled_model.counted_json == '{}':
        return HttpResponse(f"URL processing was finished with errors, please call '/update/{url_id}' to try again")
    else:
        return HttpResponse(handled_model.counted_json)