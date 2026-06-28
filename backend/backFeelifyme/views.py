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

# Importar los servicios de negocio
from .services import (
    generar_arbol_sunburst,
    obtener_resumen_calendario,
    obtener_evolucion_mensual
)

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
        tree = generar_arbol_sunburst()
        return Response(tree)


class ActividadListView(APIView):
    def get(self, request):
        actividades = Actividad.objects.all()
        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)


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
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mes = request.query_params.get("mes")
        try:
            result = obtener_resumen_calendario(request.user, mes)
            return Response(result)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


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


class EvolucionMensualView(APIView):
    """
    Devuelve el conteo de emociones primarias y actividades de un mes.
    Parámetro: ?mes=YYYY-MM
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mes = request.query_params.get("mes")
        try:
            datos = obtener_evolucion_mensual(request.user, mes)
            return Response(datos)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )