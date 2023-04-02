import logging
from io import BytesIO

import requests
from django.core.files.base import ContentFile


logger = logging.getLogger(__name__)


def save_image(url: str) -> ContentFile:
    try:
        response = requests.get(url)
        if not response.ok:
            response.raise_for_status()
        fh = BytesIO()
        fh.write(response.content)
        return ContentFile(fh.getvalue())
    except (requests.HTTPError, requests.ConnectionError) as exc:
        logger.error(str(exc))
