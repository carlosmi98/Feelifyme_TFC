import logging
from datetime import timedelta, date
from collections import defaultdict
from django.utils.timezone import localtime, now
from backFeelifyme.models import Logro, LogroUsuario, RegistroDiario, EmocionRegistrada, ActividadRealizada, Emocion

logger = logging.getLogger(__name__)

class LogroService:
    @staticmethod
    def get_logros():
        """Devuelve todos los logros activos ordenados por id."""
        return Logro.objects.filter(activo=True).order_by('id')

    @staticmethod
    def obtener_estadisticas_usuario(user) -> dict:
        """Calcula todas las estadísticas de comportamiento del usuario necesarias para evaluar logros."""
        stats = {
            "dias_racha": 0,
            "emociones_registradas": 0,
            "emociones_distintas": 0,
            "emociones_grupos_completos": False,
            "emociones_nivel3": 0,
            "emocion_favorita": 0,
            "balance_diario": False,
            "semana_equilibrada": False,
            "mes_equilibrada": False,
            "recuperacion": False,
            "estabilidad_10dias": False,
            "reflexiones": 0,
            "reflexion_larga": False,
            "dias_reflexiones": 0,
            "reflexion_post_emocion": False,
            "actividades": 0,
            "actividades_fisicas": 0,
            "actividades_sociales": 0,
            "actividades_relajantes": 0,
            "dias_actividades": 0,
            "actividades_varias": False,
            "actividad_post_emocion": False,
            # Recomendaciones (mocked/always 0/False por ahora)
            "recomendaciones": 0,
            "recomendaciones_ejercicio": 0,
            "recomendaciones_meditacion": 0,
            "recomendaciones_sociales": 0,
            "dias_recomendaciones": 0,
            "recomendacion_emocional": False,
            "mes_positivo": False,
            "meses_racha": 0,
            "positivas_15dias": False,
            "mes_autocuidado": False,
            "emocion_0000": False,
            "emocion_amanecer": False,
            "regreso_7dias": False,
            "emocion_cumple": False,
            "emocion_festivo": False,
        }

        # 1. Obtener registros y ordenarlos
        registros_qs = RegistroDiario.objects.filter(usuario=user).prefetch_related(
            'emociones_registradas__emocion',
            'actividades_realizadas__actividad'
        )
        registros = list(registros_qs)
        if not registros:
            return stats

        # Fechas de registro únicas y ordenadas ascendentemente
        dates = sorted(list(set(r.fecha for r in registros)))

        # 2. Racha máxima (dias_racha)
        max_streak = 1
        curr_streak = 1
        for i in range(1, len(dates)):
            if dates[i] - dates[i-1] == timedelta(days=1):
                curr_streak += 1
            elif dates[i] - dates[i-1] > timedelta(days=1):
                max_streak = max(max_streak, curr_streak)
                curr_streak = 1
        stats["dias_racha"] = max(max_streak, curr_streak)

        # 3. Emociones
        emociones_dict = Emocion.get_emociones_dict()
        reg_emociones = EmocionRegistrada.objects.filter(registro__usuario=user)
        stats["emociones_registradas"] = reg_emociones.count()

        unique_emociones_ids = set(re.emocion_id for re in reg_emociones)
        stats["emociones_distintas"] = len(unique_emociones_ids)

        # Primarias obtenidas (Felicidad=1, Tristeza=20, Disgusto=39, Ira=58, Miedo=77, Sorpresa=96)
        primarias_obtenidas = set()
        for eid in unique_emociones_ids:
            prim = Emocion.get_emocion_primaria(eid, emociones_dict)
            if prim:
                primarias_obtenidas.add(prim['id'])
        stats["emociones_grupos_completos"] = len(primarias_obtenidas) >= 6

        stats["emociones_nivel3"] = reg_emociones.filter(emocion__nivel='3').count()

        # Emoción favorita (máxima frecuencia de una sola emoción)
        fav_counts = defaultdict(int)
        for re in reg_emociones:
            fav_counts[re.emocion_id] += 1
        stats["emocion_favorita"] = max(fav_counts.values()) if fav_counts else 0

        # Balance diario, semanas/meses equilibrados, recuperación, meses racha, positivas 15 dias, etc.
        # Agrupar emociones primarias por registro/fecha
        day_prims = defaultdict(set)
        for r in registros:
            for er in r.emociones_registradas.all():
                prim = Emocion.get_emocion_primaria(er.emocion_id, emociones_dict)
                if prim:
                    day_prims[r.fecha].add(prim['id'])

        # Balance Diario: positivo (ID 1) y negativo (IDs 20, 39, 58, 77) el mismo día
        for fecha, prims in day_prims.items():
            has_pos = 1 in prims
            has_neg = any(nid in prims for nid in [20, 39, 58, 77])
            if has_pos and has_neg:
                stats["balance_diario"] = True
                break

        # Semana Equilibrada (al menos 4 distintas en 7 días)
        sorted_dates_with_emotions = sorted(list(day_prims.keys()))
        for i in range(len(sorted_dates_with_emotions)):
            window_prims = set()
            start_d = sorted_dates_with_emotions[i]
            for j in range(i, len(sorted_dates_with_emotions)):
                d = sorted_dates_with_emotions[j]
                if d - start_d <= timedelta(days=6):
                    window_prims.update(day_prims[d])
                else:
                    break
            if len(window_prims) >= 4:
                stats["semana_equilibrada"] = True
                break

        # Mes Equilibrado (al menos 5 distintas en un mes natural)
        month_prims = defaultdict(set)
        for d, prims in day_prims.items():
            month_prims[(d.year, d.month)].update(prims)
        stats["mes_equilibrado"] = any(len(prims) >= 5 for prims in month_prims.values())

        # Recuperación (Negativo el día N, Positivo el día N+1)
        reg_types = []
        for d in sorted_dates_with_emotions:
            has_pos = 1 in day_prims[d]
            has_neg = any(nid in day_prims[d] for nid in [20, 39, 58, 77])
            reg_types.append((d, has_pos, has_neg))
        for i in range(len(reg_types) - 1):
            d_curr, pos_curr, neg_curr = reg_types[i]
            d_next, pos_next, neg_next = reg_types[i+1]
            if d_next - d_curr == timedelta(days=1):
                if neg_curr and not pos_curr and pos_next:
                    stats["recuperacion"] = True
                    break

        # Estabilidad 10 Días (10 días consecutivos registrando sin emociones negativas nivel 3)
        if len(dates) >= 10:
            # Obtener emociones negativas nivel 3 registradas
            bad_level3_registros_fechas = set(
                reg_emociones.filter(
                    emocion__nivel='3',
                    emocion_id__in=Emocion.objects.filter(padre_id__in=[20, 39, 58, 77]).values_list('id', flat=True)
                ).values_list('registro__fecha', flat=True)
            )
            for i in range(len(dates) - 9):
                window = dates[i:i+10]
                if window[9] - window[0] == timedelta(days=9):
                    if not any(d in bad_level3_registros_fechas for d in window):
                        stats["estabilidad_10dias"] = True
                        break

        # 4. Reflexiones
        reflexiones_regs = [r for r in registros if r.notas and r.notas.strip()]
        stats["reflexiones"] = len(reflexiones_regs)
        stats["reflexion_larga"] = any(len(r.notas) > 300 for r in reflexiones_regs)

        # Racha de reflexiones
        ref_dates = sorted(list(set(r.fecha for r in reflexiones_regs)))
        max_ref_streak = 0
        if ref_dates:
            max_ref_streak = 1
            curr_ref = 1
            for i in range(1, len(ref_dates)):
                if ref_dates[i] - ref_dates[i-1] == timedelta(days=1):
                    curr_ref += 1
                elif ref_dates[i] - ref_dates[i-1] > timedelta(days=1):
                    max_ref_streak = max(max_ref_streak, curr_ref)
                    curr_ref = 1
            max_ref_streak = max(max_ref_streak, curr_ref)
        stats["dias_reflexiones"] = max_ref_streak

        # Reflexión post emoción intensa (escribir nota en un registro con nivel 3)
        stats["reflexion_post_emocion"] = any(
            any(er.emocion.nivel == '3' for er in r.emociones_registradas.all())
            for r in reflexiones_regs
        )

        # 5. Actividades
        stats["actividades"] = ActividadRealizada.objects.filter(registro__usuario=user).count()
        stats["actividades_fisicas"] = ActividadRealizada.objects.filter(
            registro__usuario=user,
            actividad__nombre__in=['correr', 'deporte', 'caminar']
        ).count()
        stats["actividades_sociales"] = ActividadRealizada.objects.filter(
            registro__usuario=user,
            actividad__nombre='socializar'
        ).count()
        stats["actividades_relajantes"] = ActividadRealizada.objects.filter(
            registro__usuario=user,
            actividad__nombre__in=['meditar', 'leer', 'cocinar', 'tocar_instrumento']
        ).count()

        # Racha de actividades
        act_dates = sorted(list(set(
            r.fecha for r in registros 
            if r.actividades_realizadas.exists()
        )))
        max_act_streak = 0
        if act_dates:
            max_act_streak = 1
            curr_act = 1
            for i in range(1, len(act_dates)):
                if act_dates[i] - act_dates[i-1] == timedelta(days=1):
                    curr_act += 1
                elif act_dates[i] - act_dates[i-1] > timedelta(days=1):
                    max_act_streak = max(max_act_streak, curr_act)
                    curr_act = 1
            max_act_streak = max(max_act_streak, curr_act)
        stats["dias_actividades"] = max_act_streak

        # Actividades varias (al menos 5 distintas en total)
        distinct_acts = ActividadRealizada.objects.filter(registro__usuario=user).values('actividad').distinct().count()
        stats["actividades_varias"] = distinct_acts >= 5

        # Actividad post emoción (actividad y emoción nivel 3 en el mismo registro)
        stats["actividad_post_emocion"] = any(
            r.actividades_realizadas.exists() and any(er.emocion.nivel == '3' for er in r.emociones_registradas.all())
            for r in registros
        )

        # 6. Mes positivo (conteo positivo > negativo)
        month_pos_neg = defaultdict(lambda: {"pos": 0, "neg": 0})
        for d, prims in day_prims.items():
            month_key = (d.year, d.month)
            if 1 in prims:
                month_pos_neg[month_key]["pos"] += 1
            if any(nid in prims for nid in [20, 39, 58, 77]):
                month_pos_neg[month_key]["neg"] += 1
        stats["mes_positivo"] = any(c["pos"] > c["neg"] for c in month_pos_neg.values())

        # Racha de meses consecutivos
        months = sorted(list(set((d.year, d.month) for d in dates)))
        max_month_streak = 0
        if months:
            max_month_streak = 1
            curr_m = 1
            for i in range(1, len(months)):
                y1, m1 = months[i-1]
                y2, m2 = months[i]
                if (y2 * 12 + m2) - (y1 * 12 + m1) == 1:
                    curr_m += 1
                else:
                    max_month_streak = max(max_month_streak, curr_m)
                    curr_m = 1
            max_month_streak = max(max_month_streak, curr_m)
        stats["meses_racha"] = max_month_streak

        # Positivas 15 días (15 días consecutivos con al menos una emoción positiva)
        pos_dates = sorted(list(set(
            fecha for fecha, prims in day_prims.items() if 1 in prims
        )))
        if len(pos_dates) >= 15:
            for i in range(len(pos_dates) - 14):
                if pos_dates[i+14] - pos_dates[i] == timedelta(days=14):
                    stats["positivas_15dias"] = True
                    break

        # Mes completo de autocuidado (emoción, actividad y reflexión en el mismo mes)
        month_care = defaultdict(lambda: {"emo": False, "act": False, "ref": False})
        for r in registros:
            m_key = (r.fecha.year, r.fecha.month)
            if r.emociones_registradas.exists():
                month_care[m_key]["emo"] = True
            if r.actividades_realizadas.exists():
                month_care[m_key]["act"] = True
            if r.notas and r.notas.strip():
                month_care[m_key]["ref"] = True
        stats["mes_autocuidado"] = any(c["emo"] and c["act"] and c["ref"] for c in month_care.values())

        # 7. Horarios y especiales
        # Emoción a medianoche (hora=0, minuto=0)
        stats["emocion_0000"] = registros_qs.filter(created_at__hour=0, created_at__minute=0).exists()

        # Emoción al amanecer (antes de las 06:00)
        stats["emocion_amanecer"] = registros_qs.filter(created_at__hour__lt=6).exists()

        # Regreso tras 7 días de inactividad
        if len(dates) >= 2:
            for i in range(1, len(dates)):
                if dates[i] - dates[i-1] >= timedelta(days=7):
                    stats["regreso_7dias"] = True
                    break

        # Cumpleaños (signup anniversary)
        anniversary = user.date_joined.date()
        stats["emocion_cumple"] = any(d.month == anniversary.month and d.day == anniversary.day for d in dates)

        # Festivos nacionales
        festivos = [
            (1, 1),   # Año Nuevo
            (1, 6),   # Epifanía
            (5, 1),   # Fiesta del Trabajo
            (8, 15),  # Asunción de la Virgen
            (10, 12), # Fiesta Nacional de España
            (11, 1),  # Todos los Santos
            (12, 6),  # Día de la Constitución
            (12, 8),  # Inmaculada Concepción
            (12, 25), # Navidad
        ]
        stats["emocion_festivo"] = any((d.month, d.day) in festivos for d in dates)

        return stats

    @staticmethod
    def evaluar_requisito(requisito: str, stats: dict) -> bool:
        """Parsea y evalúa la condición de logro string contra el diccionario de estadísticas."""
        if not requisito:
            return False
        
        req = requisito.strip()
        try:
            if '>=' in req:
                key, val_str = req.split('>=')
                key = key.strip()
                val = int(val_str.strip())
                return stats.get(key, 0) >= val
            elif '=' in req:
                key, val_str = req.split('=')
                key = key.strip()
                val_str = val_str.strip().upper()
                val = True if val_str in ('TRUE', '1') else False
                return bool(stats.get(key)) == val
        except Exception as e:
            logger.error(f"Error evaluando requisito '{requisito}': {e}")
        
        return False

    @classmethod
    def check_and_unlock(cls, user) -> list:
        """Evalúa todos los logros activos y desbloquea los que cumpla el usuario.
        Retorna la lista de objetos Logro recién desbloqueados."""
        stats = cls.obtener_estadisticas_usuario(user)
        logros_activos = Logro.objects.filter(activo=True)
        logros_usuario_ids = set(LogroUsuario.objects.filter(usuario=user).values_list('logro_id', flat=True))
        
        nuevos_logros = []
        for logro in logros_activos:
            if logro.id not in logros_usuario_ids:
                if cls.evaluar_requisito(logro.requisito, stats):
                    # Desbloquear logro
                    LogroUsuario.objects.create(usuario=user, logro=logro)
                    nuevos_logros.append({
                        "id": logro.id,
                        "nombre": logro.nombre,
                        "descripcion": logro.descripcion,
                        "tipo": logro.tipo,
                        "puntos": logro.puntos,
                    })
                    
        return nuevos_logros
