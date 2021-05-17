from django.conf import settings


def add_variable_to_context(request):
    return {
        'debug': settings.DEBUG
    }