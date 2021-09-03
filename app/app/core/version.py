from fastapi import Response

from app import get_version


def endpoint():
    return get_version() or Response(status_code=404)
