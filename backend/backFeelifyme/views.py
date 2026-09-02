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
            from .services import LogroService
            nuevos_logros = LogroService.check_and_unlock(request.user)
            return Response({
                "message": "Registro creado correctamente",
                "nuevos_logros": nuevos_logros
            }, status=status.HTTP_201_CREATED)

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


class UserLogrosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .services import LogroService
        from .models import LogroUsuario, RegistroDiario, Logro
        from datetime import timedelta
        from django.utils.timezone import localtime, now
        
        user = request.user
        
        # 1. Obtener todas las estadísticas calculadas
        stats = LogroService.obtener_estadisticas_usuario(user)
        
        # 2. Obtener logros del usuario (desbloqueados)
        logros_usuario = LogroUsuario.objects.filter(usuario=user).select_related('logro')
        desbloqueados_dict = {lu.logro_id: lu.fecha_obtenido for lu in logros_usuario}
        
        # 3. Obtener todos los logros activos
        logros_activos = Logro.objects.filter(activo=True).order_by('id')
        
        desbloqueados_data = []
        no_desbloqueados_data = []
        puntos_totales = 0
        
        for logro in logros_activos:
            is_unlocked = logro.id in desbloqueados_dict
            if is_unlocked:
                puntos_totales += logro.puntos
                desbloqueados_data.append({
                    "id": logro.id,
                    "nombre": logro.nombre,
                    "descripcion": logro.descripcion,
                    "tipo": logro.tipo,
                    "categoria": logro.categoria,
                    "dificultad": logro.dificultad,
                    "puntos": logro.puntos,
                    "requisito": logro.requisito,
                    "es_secreto": logro.es_secreto,
                    "fecha_obtenido": desbloqueados_dict[logro.id]
                })
            else:
                nombre_display = "???" if logro.es_secreto else logro.nombre
                descripcion_display = "Desbloquea este logro secreto para descubrirlo." if logro.es_secreto else logro.descripcion
                no_desbloqueados_data.append({
                    "id": logro.id,
                    "nombre": nombre_display,
                    "descripcion": descripcion_display,
                    "tipo": logro.tipo,
                    "categoria": logro.categoria,
                    "dificultad": logro.dificultad,
                    "puntos": logro.puntos,
                    "requisito": logro.requisito if not logro.es_secreto else None,
                    "es_secreto": logro.es_secreto
                })
                
        # Calcular racha activa (actual consecutiva)
        today = localtime(now()).date()
        yesterday = today - timedelta(days=1)
        dates = sorted(list(set(RegistroDiario.objects.filter(usuario=user).values_list('fecha', flat=True))))
        
        racha_activa = 0
        if dates:
            last_date = dates[-1]
            if last_date == today or last_date == yesterday:
                racha_activa = 1
                for i in range(len(dates) - 2, -1, -1):
                    if dates[i+1] - dates[i] == timedelta(days=1):
                        racha_activa += 1
                    else:
                        break
                        
        response_data = {
            "desbloqueados": desbloqueados_data,
            "no_desbloqueados": no_desbloqueados_data,
            "puntos_totales": puntos_totales,
            "racha_actual": racha_activa,
            "reflexiones_count": stats.get("reflexiones", 0),
            "recomendaciones_count": 0
        }
        
        return Response(response_data)
