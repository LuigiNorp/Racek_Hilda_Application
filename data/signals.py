from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models

@receiver(pre_save)
def capitalize_text_fields(sender, instance, **kwargs):
    if hasattr(sender, '_meta'):
        for field in instance._meta.fields:
            if isinstance(field, models.CharField) and field.name != "id":
                value = getattr(instance, field.name)
                if value:
                    setattr(instance, field.name, value.upper())
