from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer, UserSerializer, ActividadSerializer, 
    RegistroDiarioCreateSerializer, RegistroDiarioSerializer,
    EmocionRegistradaSerializer, ActividadRealizadaSerializer
)
from rest_framework import status
from backFeelifyme.models import Emocion, Actividad, RegistroDiario, EmocionRegistrada, ActividadRealizada
from rest_framework import viewsets, exceptions
from django.utils.timezone import localtime, now
import calendar
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Caché en memoria del árbol de emociones
# Las 113 emociones son inmutables: se cargan UNA sola vez al primer uso y
# permanecen en RAM. Navegar el árbol para encontrar la raíz (nivel="1")
# es puro Python, sin queries adicionales a la base de datos.
# ---------------------------------------------------------------------------
_EMOCIONES_CACHE: dict | None = None


def _get_emociones_dict() -> dict:
    """Devuelve el dict {id: {id, nombre, nivel, padre_id}} cargando desde
    la BD solo si todavía no está en caché."""
    global _EMOCIONES_CACHE
    if _EMOCIONES_CACHE is None:
        _EMOCIONES_CACHE = {
            e.id: {
                "id": e.id,
                "nombre": e.nombre,
                "nivel": e.nivel,
                "padre_id": e.padre_id,
            }
            for e in Emocion.objects.all()
        }
    return _EMOCIONES_CACHE


def _get_emocion_primaria(emocion_id: int, emociones_dict: dict) -> dict | None:
    """Sube por el árbol en memoria hasta encontrar la emoción de nivel '1'.
    Máximo 2 saltos (3→2→1). Devuelve {id, nombre} o None si no se encuentra."""
    emocion = emociones_dict.get(emocion_id)
    while emocion and emocion["nivel"] != "1":
        emocion = emociones_dict.get(emocion["padre_id"])
    return emocion


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Usuario creado correctamente"},
            status=status.HTTP_201_CREATED
        )

        
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.delete() 
        return Response({"message": "Cuenta eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)

class EmocionTreeView(APIView):
    """
    Endpoint público que devuelve las emociones en un formato de árbol (Sunburst)
    ideal para la librería @nivo/sunburst en React.
    """
    def get(self, request):
        emociones = Emocion.objects.all()
        
        # Crear un diccionario temporal para estructurar de manera eficiente el árbol
        emocion_dict = {}
        for em in emociones:
            emocion_dict[em.id] = {
                "id": em.id,
                "name": em.nombre,
                "nivel": em.nivel,
                "children": []
            }

        # Armar las relaciones estructuradas (hijo dentro de padre)
        for em in emociones:
            if em.padre_id and em.padre_id in emocion_dict:
                emocion_dict[em.padre_id]["children"].append(emocion_dict[em.id])

        # Extraer únicamente los que son del núcleo (Nivel 1 o sin padre) para el nivel superior
        root_children = [item for em_id, item in emocion_dict.items() if item["nivel"] == "1"]
        
        # Añadir la propiedad "loc" a los nodos "hoja" (último nivel),
        # ya que nivo la necesita para saber el tamaño de las porciones finales de la tarta.
        def assign_loc_to_leaves(node):
            if len(node["children"]) == 0:
                node["loc"] = 1
                del node["children"] # Eliminamos children si está vacío
            else:
                for child in node["children"]:
                    assign_loc_to_leaves(child)

        for root_node in root_children:
            assign_loc_to_leaves(root_node)

        # Retornamos el objeto final al estilo que nivo espera (un root con un array de hijos)
        tree = {
            "name": "root",
            "children": root_children
        }

        return Response(tree)

class ActividadListView(APIView):

    def get(self, request):
        actividades = Actividad.objects.all()
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)

# Nueva view con la intención de hacer un resumen cronologico de las emociones y actividades del dia
class ResumenDiarioCronologicoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fecha = request.query_params.get("fecha")

        registros = RegistroDiario.objects.filter(
            usuario=request.user,
            fecha=fecha
        ).order_by("created_at")

        data = {
            "fecha": fecha,
            "registros": []
        }

        for registro in registros:
            emociones = EmocionRegistrada.objects.filter(
                registro=registro
            ).select_related("emocion")

            actividades = ActividadRealizada.objects.filter(
                registro=registro
            ).select_related("actividad")

            data["registros"].append({
                "id": registro.id,
                "hora": localtime(registro.created_at).time(),
                "emociones": [
                    {"id": e.emocion.id, "nombre": e.emocion.nombre}
                    for e in emociones
                ],
                "actividades": [
                    {"id": a.actividad.id, "nombre": a.actividad.nombre}
                    for a in actividades
                ],
                "notas": registro.notas
            })

        return Response(data)


class CalendarioResumenMesView(APIView):
    """
    Devuelve el resumen de emociones primarias y actividades preview
    para cada día del mes solicitado.

    Parámetro: ?mes=YYYY-MM  (ej. ?mes=2026-04)

    Coste: 1 query para el caché de emociones (solo la primera vez) +
           1 query con prefetch_related para registros, emociones y actividades.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mes = request.query_params.get("mes")
        if not mes:
            return Response(
                {"error": "Parámetro 'mes' requerido. Formato: YYYY-MM."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            año, mes_num = map(int, mes.split("-"))
            primer_dia = date(año, mes_num, 1)
            ultimo_dia = date(año, mes_num, calendar.monthrange(año, mes_num)[1])
        except (ValueError, AttributeError):
            return Response(
                {"error": "Formato de mes inválido. Usa YYYY-MM."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Caché en memoria: 0 queries extra tras la primera petición
        emociones_dict = _get_emociones_dict()

        # Una sola query con prefetch — sin N+1
        registros = RegistroDiario.objects.filter(
            usuario=request.user,
            fecha__range=[primer_dia, ultimo_dia]
        ).prefetch_related(
            "emociones_registradas__emocion",
            "actividades_realizadas__actividad",
        )

        # Agrupar por fecha usando dicts para deduplicar automáticamente
        resumen: dict[str, dict] = {}
        for registro in registros:
            fecha_str = str(registro.fecha)
            if fecha_str not in resumen:
                resumen[fecha_str] = {
                    "emociones_primarias": {},  # {id: {id, nombre}} — sin duplicados
                    "actividades_preview": {},  # {id: {id, nombre}} — sin duplicados
                }

            for er in registro.emociones_registradas.all():
                primaria = _get_emocion_primaria(er.emocion.id, emociones_dict)
                if primaria:
                    resumen[fecha_str]["emociones_primarias"][primaria["id"]] = {
                        "id": primaria["id"],
                        "nombre": primaria["nombre"],
                    }

            for ar in registro.actividades_realizadas.all():
                act = ar.actividad
                resumen[fecha_str]["actividades_preview"][act.id] = {
                    "id": act.id,
                    "nombre": act.nombre,
                }

        # Construir la lista de días del mes
        result = []
        current = primer_dia
        while current <= ultimo_dia:
            fecha_str = str(current)
            dia = resumen.get(fecha_str)
            result.append({
                "fecha": fecha_str,
                "tiene_registro": dia is not None,
                "emociones_primarias": list(dia["emociones_primarias"].values()) if dia else [],
                # Máximo 3 actividades en la preview de la casilla
                "actividades_preview": list(dia["actividades_preview"].values())[:3] if dia else [],
            })
            current += timedelta(days=1)

        return Response(result)


class RegistroDiarioViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroDiarioSerializer
    permission_classes = [IsAuthenticated]

    # Que solo vea sus propios registros
    def get_queryset(self):
        return RegistroDiario.objects.filter(usuario=self.request.user)

    # Interceptar el Borrado actual
    def perform_destroy(self, instance):
        if instance.fecha != localtime(now()).date():
            raise exceptions.PermissionDenied("Solo puedes borrar registros del día actual.")
        instance.delete()

    # Interceptar la Actualización actual
    def perform_update(self, serializer):
        if serializer.instance.fecha != localtime(now()).date():
            raise exceptions.PermissionDenied("Solo puedes editar registros del día actual.")
        serializer.save()


class CrearRegistroDiario(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RegistroDiarioCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            registro = serializer.save()
            return Response({"message": "Registro creado correctamente"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Borrar exponer datos innecesarios no se va a usar en ningun sitio solo se creó con la intención de hacer pruebas en postman antes de implementar front
#class EmocionRegistradaListView(APIView):
#    permission_classes = [IsAuthenticated]

#    def get(self, request):
#        emociones = EmocionRegistrada.objects.filter(registro__usuario=request.user)
#        serializer = EmocionRegistradaSerializer(emociones, many=True)
#        return Response(serializer.data)

# Borrar exponer datos innecesarios no se va a usar en ningun sitio solo se creó con la intención de hacer pruebas en postman antes de implementar front
#class ActividadRealizadaListView(APIView):
#    permission_classes = [IsAuthenticated]

#    def get(self, request):
#        actividades = ActividadRealizada.objects.filter(registro__usuario=request.user)
#        serializer = ActividadRealizadaSerializer(actividades, many=True)
#        return Response(serializer.data)