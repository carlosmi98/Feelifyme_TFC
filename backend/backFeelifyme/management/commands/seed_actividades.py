# Generated seed_actividades.py
from django.core.management.base import BaseCommand
from backFeelifyme.models import Actividad

ACTIVIDADES_DATA = [{'model': 'backFeelifyme.actividad', 'pk': 1, 'fields': {'nombre': 'caminar', 'categoria': 'fisica'}}, {'model': 'backFeelifyme.actividad', 'pk': 2, 'fields': {'nombre': 'cocinar', 'categoria': 'creativa'}}, {'model': 'backFeelifyme.actividad', 'pk': 3, 'fields': {'nombre': 'correr', 'categoria': 'fisica'}}, {'model': 'backFeelifyme.actividad', 'pk': 4, 'fields': {'nombre': 'deporte', 'categoria': 'fisica'}}, {'model': 'backFeelifyme.actividad', 'pk': 5, 'fields': {'nombre': 'socializar', 'categoria': 'social'}}, {'model': 'backFeelifyme.actividad', 'pk': 6, 'fields': {'nombre': 'tocar_instrumento', 'categoria': 'creativa'}}, {'model': 'backFeelifyme.actividad', 'pk': 7, 'fields': {'nombre': 'leer', 'categoria': 'creativa'}}, {'model': 'backFeelifyme.actividad', 'pk': 8, 'fields': {'nombre': 'meditar', 'categoria': 'bienestar'}}, {'model': 'backFeelifyme.actividad', 'pk': 9, 'fields': {'nombre': 'bailar', 'categoria': 'fisica'}}, {'model': 'backFeelifyme.actividad', 'pk': 10, 'fields': {'nombre': 'yoga', 'categoria': 'fisica'}}, {'model': 'backFeelifyme.actividad', 'pk': 11, 'fields': {'nombre': 'descansar', 'categoria': 'bienestar'}}, {'model': 'backFeelifyme.actividad', 'pk': 12, 'fields': {'nombre': 'jardinería', 'categoria': 'bienestar'}}, {'model': 'backFeelifyme.actividad', 'pk': 13, 'fields': {'nombre': 'limpieza', 'categoria': 'bienestar'}}, {'model': 'backFeelifyme.actividad', 'pk': 14, 'fields': {'nombre': 'escribir', 'categoria': 'creativa'}}, {'model': 'backFeelifyme.actividad', 'pk': 15, 'fields': {'nombre': 'fotografiar', 'categoria': 'creativa'}}, {'model': 'backFeelifyme.actividad', 'pk': 16, 'fields': {'nombre': 'pintar', 'categoria': 'creativa'}}, {'model': 'backFeelifyme.actividad', 'pk': 17, 'fields': {'nombre': 'cine_series', 'categoria': 'digital'}}, {'model': 'backFeelifyme.actividad', 'pk': 18, 'fields': {'nombre': 'jugar_videojuegos', 'categoria': 'digital'}}, {'model': 'backFeelifyme.actividad', 'pk': 19, 'fields': {'nombre': 'llamar_ser_querido', 'categoria': 'digital'}}, {'model': 'backFeelifyme.actividad', 'pk': 20, 'fields': {'nombre': 'estudiar', 'categoria': 'productiva'}}, {'model': 'backFeelifyme.actividad', 'pk': 21, 'fields': {'nombre': 'planificar', 'categoria': 'productiva'}}, {'model': 'backFeelifyme.actividad', 'pk': 22, 'fields': {'nombre': 'trabajar', 'categoria': 'productiva'}}, {'model': 'backFeelifyme.actividad', 'pk': 23, 'fields': {'nombre': 'ayudar', 'categoria': 'social'}}, {'model': 'backFeelifyme.actividad', 'pk': 24, 'fields': {'nombre': 'recados', 'categoria': 'cotidiana'}}]

class Command(BaseCommand):
    help = 'Carga las 24 actividades categorizadas de forma idempotente.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando actividades...')
        
        creadas = 0
        actualizadas = 0

        for item in ACTIVIDADES_DATA:
            fields = item['fields']
            nombre = fields['nombre']
            categoria = fields.get('categoria', 'cotidiana')

            obj, created = Actividad.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categoria
                }
            )

            if not created:
                obj.categoria = categoria
                obj.save()
                actualizadas += 1
            else:
                creadas += 1

        self.stdout.write(self.style.SUCCESS(f'[OK] Actividades cargadas: {creadas} creadas, {actualizadas} actualizadas.'))
