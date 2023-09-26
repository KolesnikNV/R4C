from rest_framework import status
from rest_framework.response import Response


def get_or_create_model(model, **kwargs):
    instance, created = model.objects.get_or_create(**kwargs)
    return instance, created


def filter_model(model, **kwargs):
    return model.objects.filter(**kwargs)


def bad_request_response(message):
    return Response(
        {"error": f"{message}"},
        status=status.HTTP_400_BAD_REQUEST,
    )
