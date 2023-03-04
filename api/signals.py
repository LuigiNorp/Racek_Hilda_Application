# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.exceptions import ValidationError
# from .models import *

# @receiver(pre_save, sender=Curp)
# def verificar_curp_data(sender, instance, **kwargs):
#     curp = instance.curp
#     try:
#         objeto = Curp.objects.get(curp=curp)
#         raise ValidationError("El registro ya existe en la base de datos")
#     except Curp.DoesNotExist:
#         pass

# @receiver(pre_save, sender=Curp)
# def verificar_curp_data(sender, instance, **kwargs):
#     curp_data = instance.curp_data
#     try:
#         objeto = Curp.objects.get(curp_data=curp_data)
#         raise ValidationError("El registro ya existe en la base de datos")
#     except Curp.DoesNotExist:
#         pass