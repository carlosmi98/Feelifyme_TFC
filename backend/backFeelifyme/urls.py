from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView,
    MeView,
    EmocionTreeView,
    ActividadListView,
    CrearRegistroDiario,
    ResumenDiarioCronologicoView,
    CalendarioResumenMesView,
    RegistroDiarioViewSet,
    EvolucionMensualView,
    UserLogrosView,
)

router = DefaultRouter()
router.register(r"registros-edicion", RegistroDiarioViewSet, basename="edicion-registros")

urlpatterns = [
    # usuarios
    path("users/register/", RegisterView.as_view(), name="register"),
    path("users/login/", TokenObtainPairView.as_view(), name="login"),
    path("users/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("users/me/", MeView.as_view(), name="me"),

    # Emociones
    path("emociones/arbol/", EmocionTreeView.as_view(), name="emociones-arbol"),

    # Actividades
    path("actividades/", ActividadListView.as_view(), name="actividades"),

    # registro diario
    path("registro-diario/", CrearRegistroDiario.as_view(), name="crear-registro-diario"),
    path("resumen-dia/", ResumenDiarioCronologicoView.as_view(), name="resumen-dia"),

    # Calendario
    # GET /api/calendario/resumen/?mes=YYYY-MM
    path("calendario/resumen/", CalendarioResumenMesView.as_view(), name="calendario-resumen"),

    # viewSet edición (put / delete del día actual)
    # /api/registros-edicion/<id>/
    path("", include(router.urls)),

    # Evolucion Mensual
    path("evolucion/mensual/", EvolucionMensualView.as_view(), name="evolucion-mensual"),

    # Logros
    path("users/me/logros/", UserLogrosView.as_view(), name="user-logros"),
]
