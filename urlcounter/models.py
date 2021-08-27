from typing import Union
from django.db import models


class url_model(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField()
    counted_json = models.JSONField()

    @staticmethod
    def get_existing_id(url_str) -> Union[int, None]:
        try:
            existing_model = url_model.objects.get(url=url_str)
            return existing_model.id
        except models.ObjectDoesNotExist:
            return None
