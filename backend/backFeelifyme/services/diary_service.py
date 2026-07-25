import calendar
from datetime import date, timedelta
from backFeelifyme.models import Emocion, RegistroDiario

def generar_arbol_sunburst() -> dict:
    """
    Construye las emociones en un formato de árbol (Sunburst)
    ideal para la librería @nivo/sunburst en React.
    """
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
    return {
        "name": "root",
        "children": root_children
    }


def obtener_resumen_calendario(usuario, mes_str: str) -> list:
    """
    Devuelve el resumen de emociones primarias y actividades preview
    para cada día del mes solicitado.
    """
    if not mes_str:
        raise ValueError("Parámetro 'mes' requerido. Formato: YYYY-MM.")

    try:
        año, mes_num = map(int, mes_str.split("-"))
        primer_dia = date(año, mes_num, 1)
        ultimo_dia = date(año, mes_num, calendar.monthrange(año, mes_num)[1])
    except (ValueError, AttributeError):
        raise ValueError("Formato de mes inválido. Usa YYYY-MM.")

    # Caché en memoria encapsulado en Emocion
    emociones_dict = Emocion.get_emociones_dict()

    # Una sola query con prefetch — sin N+1
    registros = RegistroDiario.objects.filter(
        usuario=usuario,
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
            primaria = Emocion.get_emocion_primaria(er.emocion.id, emociones_dict)
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

    return result


def obtener_evolucion_mensual(usuario, mes_str: str) -> dict:
    """
    Devuelve el conteo de emociones primarias y actividades de un mes.
    """
    if not mes_str:
        raise ValueError("Parámetro 'mes' requerido. Formato: YYYY-MM.")

    try:
        año, mes_num = map(int, mes_str.split("-"))
        primer_dia = date(año, mes_num, 1)
        ultimo_dia = date(año, mes_num, calendar.monthrange(año, mes_num)[1])
    except (ValueError, AttributeError):
        raise ValueError("Formato de mes inválido. Usa YYYY-MM.")

    emociones_dict = Emocion.get_emociones_dict()

    registros = RegistroDiario.objects.filter(
        usuario=usuario,
        fecha__range=[primer_dia, ultimo_dia]
    ).prefetch_related(
        "emociones_registradas__emocion",
        "actividades_realizadas__actividad",
    )

    conteo_emociones = {}
    conteo_actividades = {}

    for registro in registros:
        # Emociones
        emociones_primarias_del_registro = set()
        for er in registro.emociones_registradas.all():
            primaria = Emocion.get_emocion_primaria(er.emocion.id, emociones_dict)
            if primaria:
                emociones_primarias_del_registro.add(primaria["nombre"])
        
        for nombre_primaria in emociones_primarias_del_registro:
            if nombre_primaria not in conteo_emociones:
                conteo_emociones[nombre_primaria] = 0
            conteo_emociones[nombre_primaria] += 1
            
        # Actividades
        for ar in registro.actividades_realizadas.all():
            nombre_actividad = ar.actividad.nombre
            if nombre_actividad not in conteo_actividades:
                conteo_actividades[nombre_actividad] = 0
            conteo_actividades[nombre_actividad] += 1

    # Ordenar actividades de mayor a menor frecuencia para el gráfico de barras
    actividades_ordenadas = sorted(conteo_actividades.items(), key=lambda item: item[1], reverse=False)

    formato_emociones = [{"name": k, "value": v} for k, v in conteo_emociones.items()]
    formato_actividades = [{"name": k, "value": v} for k, v in actividades_ordenadas]

    return {
        "emociones": formato_emociones,
        "actividades": formato_actividades
    }
