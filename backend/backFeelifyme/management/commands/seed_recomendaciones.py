import sys
from django.core.management.base import BaseCommand
from backFeelifyme.models import Recomendacion, Emocion, Actividad, RecomendacionEmocion

RECOMENDACIONES_DATA = [
    # 🔴 CALMA (Miedo, Ansiedad, Estrés, Disgusto)
    {
        "titulo": "Respiración 4-7-8 para Calmar la Mente",
        "descripcion": "Una técnica de respiración rítmica diseñada para desacelerar la frecuencia cardíaca y calmar el sistema nervioso.",
        "tipo": "calma",
        "consejo_rapido": "Inhala en 4s, mantén 7s y exhala suavemente en 8s.",
        "duracion": "3 min",
        "pasos": [
            "1. Siéntate cómodamente con la espalda recta.",
            "2. Inhala por la nariz silenciosamente durante 4 segundos.",
            "3. Mantén la respiración durante 7 segundos.",
            "4. Exhala por la boca haciendo un suave sonido durante 8 segundos.",
            "5. Repite el ciclo 4 veces consecutivas."
        ],
        "emociones": ["miedo", "ira", "disgusto"],
        "actividad": "meditar"
    },
    {
        "titulo": "Apagado Digital Nocturno",
        "descripcion": "Desconecta las pantallas antes de dormir para reducir la sobreestimulación visual y facilitar un descanso profundo.",
        "tipo": "calma",
        "consejo_rapido": "Apaga o aleja tus pantallas 30 minutos antes de acostarte.",
        "duracion": "5 min",
        "pasos": [
            "1. Activa el modo 'No molestar' en tu teléfono.",
            "2. Deja los dispositivos fuera de tu alcance desde la cama.",
            "3. Ajusta una luz tenue en tu habitación.",
            "4. Lee un libro físico o realiza respiraciones lentas antes de cerrar los ojos."
        ],
        "emociones": ["miedo", "disgusto"],
        "actividad": "descansar"
    },
    {
        "titulo": "Técnica de Anclaje Grounding 5-4-3-2-1",
        "descripcion": "Ejercicio sensorial para reconectar con el presente y salir de bucles de pensamientos ansiosos.",
        "tipo": "calma",
        "consejo_rapido": "Nombra 5 cosas que ves, 4 que tocas, 3 que oyes, 2 que hueles y 1 que saboreas.",
        "duracion": "4 min",
        "pasos": [
            "1. Observa y nombra 5 cosas visibles a tu alrededor.",
            "2. Identifica y toca 4 texturas cercanas.",
            "3. Escucha con atención 3 sonidos del ambiente.",
            "4. Reconoce 2 olores presentes.",
            "5. Siente 1 sabor en tu boca."
        ],
        "emociones": ["miedo"],
        "actividad": "meditar"
    },
    {
        "titulo": "Escaneo Corporal Breve",
        "descripcion": "Recorrido mental por tu cuerpo para identificar y soltar áreas de tensión muscular.",
        "tipo": "calma",
        "consejo_rapido": "Lleva tu atención desde los pies hasta la cabeza soltando rigideces.",
        "duracion": "5 min",
        "pasos": [
            "1. Cierra los ojos e inhala profundamente.",
            "2. Enfoca tu mente en tus pies y piernas, soltando cualquier tensión al exhalar.",
            "3. Sube la atención hacia el abdomen, pecho y hombros.",
            "4. Relaja la mandíbula y el entrecejo."
        ],
        "emociones": ["miedo", "ira"],
        "actividad": "yoga"
    },
    {
        "titulo": "Infusión Consciente",
        "descripcion": "Prepara una bebida caliente utilizando tus cinco sentidos como pausa de serenidad.",
        "tipo": "calma",
        "consejo_rapido": "Disfruta el aroma y el calor de una taza sin distracciones digitales.",
        "duracion": "5 min",
        "pasos": [
            "1. Hierve agua y elige una infusión reconfortante.",
            "2. Observa el vapor subiendo y huele las hierbas.",
            "3. Sostén la taza sintiendo su calor en tus manos.",
            "4. Da pequeños sorbos saboreando la bebida en silencio."
        ],
        "emociones": ["disgusto", "miedo"],
        "actividad": "cocinar"
    },
    {
        "titulo": "Paseo de Desconexión Sin Pantallas",
        "descripcion": "Caminata breve al aire libre sin notificaciones para oxigenar tu mente.",
        "tipo": "calma",
        "consejo_rapido": "Camina 10 minutos sin mirar el teléfono.",
        "duracion": "5 min",
        "pasos": [
            "1. Deja el teléfono en bolsillo o mochila en silencio.",
            "2. Sal a dar una vuelta corta a ritmo suave.",
            "3. Mira hacia la copa de los árboles o el cielo.",
            "4. Respira el aire fresco sin prisa."
        ],
        "emociones": ["miedo", "tristeza"],
        "actividad": "caminar"
    },
    {
        "titulo": "Ducha de Liberación Emocional",
        "descripcion": "Utiliza el agua tibia como metáfora visual para limpiar el agotamiento del día.",
        "tipo": "calma",
        "consejo_rapido": "Siente el agua cayendo e imagina que se lleva tus preocupaciones.",
        "duracion": "5 min",
        "pasos": [
            "1. Ajusta la temperatura del agua a un nivel agradable.",
            "2. Cierra los ojos bajo el agua unos segundos.",
            "3. Visualiza que las tenciones bajan por el desagüe.",
            "4. Sécate con una toalla reconfortante."
        ],
        "emociones": ["disgusto", "tristeza"],
        "actividad": "descansar"
    },
    {
        "titulo": "Pausa de la Taza Caliente",
        "descripcion": "Pausa breve durante el trabajo para reconectar con tus sensaciones corporales.",
        "tipo": "calma",
        "consejo_rapido": "Suelta el ratón y abraza tu taza con ambas manos durante 2 minutos.",
        "duracion": "3 min",
        "pasos": [
            "1. Aléjate de la pantalla del ordenador.",
            "2. Toma tu taza con ambas manos sintiendo la temperatura.",
            "3. Haz 3 respiraciones profundas manteniendo los hombros abajo.",
            "4. Retoma tus tareas con la mente renovada."
        ],
        "emociones": ["miedo", "ira"],
        "actividad": "descansar"
    },
    {
        "titulo": "Respiración Diafragmática",
        "descripcion": "Lleva la respiración hacia la zona abdominal para reducir la respuesta de estrés.",
        "tipo": "calma",
        "consejo_rapido": "Infla tu vientre al inhalar y déjalo caer al exhalar.",
        "duracion": "4 min",
        "pasos": [
            "1. Pon una mano en el pecho y otra en el abdomen.",
            "2. Inhala intentando mover únicamente la mano del abdomen.",
            "3. Exhala despacio notando cómo desciende la mano.",
            "4. Completa 10 repeticiones profundas."
        ],
        "emociones": ["miedo"],
        "actividad": "meditar"
    },
    {
        "titulo": "Estiramiento de Cuello y Trapecios",
        "descripcion": "Relaja la zona superior de la espalda donde se acumula la tensión por ansiedad.",
        "tipo": "calma",
        "consejo_rapido": "Inclina suavemente la cabeza a cada lado sintiendo el estiramiento.",
        "duracion": "3 min",
        "pasos": [
            "1. Inclina tu oreja derecha hacia el hombro derecho manteniendo 15s.",
            "2. Repite con lentitud hacia el lado izquierdo.",
            "3. Rota los hombros en círculos amplios hacia atrás 10 veces.",
            "4. Sacude las manos con suavidad."
        ],
        "emociones": ["miedo", "ira"],
        "actividad": "yoga"
    },

    # 🔴 ENERGÍA Y PAUSA ACTIVA (Ira, Frustración, Apatía)
    {
        "titulo": "Técnica STOP para Impulsos",
        "descripcion": "Estrategia para hacer una pausa consciente antes de reaccionar con ira o frustración.",
        "tipo": "energia",
        "consejo_rapido": "Stop – Take a breath – Observe – Proceed.",
        "duracion": "2 min",
        "pasos": [
            "1. S (Stop): Detén lo que estás haciendo o diciendo.",
            "2. T (Take a breath): Toma una respiración profunda.",
            "3. O (Observe): Observa qué emoción sientes en el cuerpo sin juzgarla.",
            "4. P (Proceed): Continúa actuando con serenidad."
        ],
        "emociones": ["ira"],
        "actividad": "meditar"
    },
    {
        "titulo": "Descarga de Tensión Física",
        "descripcion": "Canaliza el exceso de adrenalina provocado por el enfado mediante el movimiento muscular intenso.",
        "tipo": "energia",
        "consejo_rapido": "Haz 20 flexiones o saltos de tijera para quemar la frustración.",
        "duracion": "5 min",
        "pasos": [
            "1. Haz 15-20 sentadillas o flexiones rápidas.",
            "2. O sal a trotar 5 minutos si dispones de espacio.",
            "3. Nota cómo baja la intensidad del enfado tras el esfuerzo.",
            "4. Recupera el aliento bébiendote un vaso de agua."
        ],
        "emociones": ["ira"],
        "actividad": "correr"
    },
    {
        "titulo": "Pausa Activa de 5 Minutos",
        "descripcion": "Rompe la rigidez física y mental cambiando radicalmente de postura.",
        "tipo": "energia",
        "consejo_rapido": "Levántate de la silla, estírate y camina por la habitación.",
        "duracion": "5 min",
        "pasos": [
            "1. Levántate de tu silla al instante.",
            "2. Estira los brazos hacia el techo lo más alto posible.",
            "3. Flexiona el tronco hacia adelante intentando tocar los pies.",
            "4. Camina unos pasos agitadamente para activar la circulación."
        ],
        "emociones": ["ira", "tristeza"],
        "actividad": "deporte"
    },
    {
        "titulo": "Bailar tu Canción Favorita",
        "descripcion": "Cambia tu estado químico cerebral moviéndote al ritmo de una música motivadora.",
        "tipo": "energia",
        "consejo_rapido": "Ponte auriculares y muévete sin juzgarte durante 3 minutos.",
        "duracion": "4 min",
        "pasos": [
            "1. Selecciona un tema musical con ritmo alegre.",
            "2. Ajusta el volumen a tu gusto.",
            "3. Muévete libremente por la estancia sin importar la técnica.",
            "4. Sonríe al finalizar el tema."
        ],
        "emociones": ["tristeza", "ira", "felicidad"],
        "actividad": "bailar"
    },
    {
        "titulo": "Estiramiento de Columna Gato-Vaca",
        "descripcion": "Moviliza la columna vertebral para soltar la rigidez provocada por la rabia.",
        "tipo": "energia",
        "consejo_rapido": "Moviliza tu espalda coordinando la inhalación con la curva lumbar.",
        "duracion": "3 min",
        "pasos": [
            "1. Colócate sobre manos y rodillas en el suelo o esterilla.",
            "2. Inhala arqueando la espalda hacia abajo y mirando hacia arriba.",
            "3. Exhala redondeando la espalda hacia el techo metiendo la barbilla.",
            "4. Completa 8 repeticiones fluidas."
        ],
        "emociones": ["ira"],
        "actividad": "yoga"
    },
    {
        "titulo": "Caminata Vigorosa",
        "descripcion": "Camina a paso ligero para liberar endorfinas y despejar la frustración.",
        "tipo": "energia",
        "consejo_rapido": "Camina a paso firme durante 10 minutos sintiendo el balanceo de tus brazos.",
        "duracion": "5 min",
        "pasos": [
            "1. Ponte calzado cómodo.",
            "2. Camina manteniendo la vista al frente y el abdomen firme.",
            "3. Aumenta el ritmo los primeros 3 minutos.",
            "4. Reduce la velocidad al final respirando hondo."
        ],
        "emociones": ["ira"],
        "actividad": "caminar"
    },
    {
        "titulo": "Sacudida Somática Corporal",
        "descripcion": "Técnica corporal para despojarse de la rigidez muscular acumulada.",
        "tipo": "energia",
        "consejo_rapido": "Sacude tus manos, brazos y piernas como si te quitaras gotas de agua.",
        "duracion": "2 min",
        "pasos": [
            "1. Ponte de pie con las rodillas flojas.",
            "2. Sacude vigorosamente tus manos y muñecas.",
            "3. Permite que el movimiento suba a hombros y piernas durante 2 minutos.",
            "4. Quédate quieto sintiendo el hormigueo revitalizante."
        ],
        "emociones": ["ira", "miedo"],
        "actividad": "deporte"
    },
    {
        "titulo": "Playlist de Alta Energía",
        "descripcion": "Escucha ritmos potentes para activar la motivación en momentos de apatía.",
        "tipo": "energia",
        "consejo_rapido": "Escucha 2 temas de música instrumental enérgica para activarte.",
        "duracion": "4 min",
        "pasos": [
            "1. Pon una lista de reproducción con ritmo ascendente.",
            "2. Cierra los ojos marcando el compás con las manos.",
            "3. Deja que la música venza la inercia del desánimo."
        ],
        "emociones": ["tristeza"],
        "actividad": "bailar"
    },
    {
        "titulo": "Estímulo con Agua Fría en el Rostro",
        "descripcion": "Activa el nervio vago para desacelerar la respuesta de rabia impulsiva.",
        "tipo": "energia",
        "consejo_rapido": "Salpica agua fría en tu rostro 4 veces seguidas.",
        "duracion": "1 min",
        "pasos": [
            "1. Acércate al lavabo y abre el agua fría.",
            "2. Salpica tu cara de 4 a 5 veces refrescando la frente.",
            "3. Mantén el agua fresca unos segundos y sécate suavemente."
        ],
        "emociones": ["ira"],
        "actividad": "descansar"
    },
    {
        "titulo": "Estiramiento Zancada del Cazador",
        "descripcion": "Abre la pelvis y el tórax liberando la rigidez en las caderas.",
        "tipo": "energia",
        "consejo_rapido": "Da un paso largo hacia adelante abriendo el pecho durante 20s.",
        "duracion": "4 min",
        "pasos": [
            "1. Da un paso largo hacia adelante doblando la rodilla delantera.",
            "2. Eleva los brazos hacia el cielo abriendo el pecho.",
            "3. Mantén la postura 20 segundos sintiendo la apertura.",
            "4. Cambia de pierna."
        ],
        "emociones": ["ira"],
        "actividad": "yoga"
    },

    # 🟢 SOCIAL Y CONEXIÓN (Tristeza, Soledad, Melancolía)
    {
        "titulo": "Micro-acción Social",
        "descripcion": "Rompe la inercia del aislamiento enviando un mensaje afectuoso a alguien cercano.",
        "tipo": "social",
        "consejo_rapido": "Envía un mensaje breve: '¡Hola! Me acordé de ti hoy, ¿cómo estás?'",
        "duracion": "2 min",
        "pasos": [
            "1. Elige una persona de tu círculo cercano.",
            "2. Escríbele un saludo cercano sin mayor compromiso.",
            "3. Disfruta la sensación de estar conectado sin presiones."
        ],
        "emociones": ["tristeza"],
        "actividad": "socializar"
    },
    {
        "titulo": "Llamada Exprés de 5 Minutos",
        "descripcion": "Conecta con la voz de un amigo o familiar para aliviar la sensación de soledad.",
        "tipo": "social",
        "consejo_rapido": "Llama a un ser querido para un intercambio breve de palabras.",
        "duracion": "5 min",
        "pasos": [
            "1. Marca el teléfono de un familiar o amigo cercano.",
            "2. Pregúntale cómo le va el día y escucha su voz.",
            "3. Comparte una pequeña nota positiva de tu jornada."
        ],
        "emociones": ["tristeza"],
        "actividad": "llamar_ser_querido"
    },
    {
        "titulo": "Expresar Gratitud Directa",
        "descripcion": "Agradece un gesto reciente a alguien para reconectar afectivamente.",
        "tipo": "social",
        "consejo_rapido": "Envía un mensaje de agradecimiento sincero a una persona especial.",
        "duracion": "3 min",
        "pasos": [
            "1. Recuerda a alguien que haya sido amable contigo últimamente.",
            "2. Redacta 2 líneas dándole las gracias sinceramente.",
            "3. Siente el beneficio mutuo del reconocimiento."
        ],
        "emociones": ["tristeza", "felicidad"],
        "actividad": "ayudar"
    },
    {
        "titulo": "Pequeño Acto de Amabilidad",
        "descripcion": "Realizar un favor sencillo a otra persona desplaza el foco de tu dolor interno.",
        "tipo": "social",
        "consejo_rapido": "Haz un pequeño favor desinteresado a un compañero o conocido.",
        "duracion": "4 min",
        "pasos": [
            "1. Identifica una oportunidad sencilla de ayudar a alguien cerca.",
            "2. Ofrece tu ayuda o sostén un detalle amable.",
            "3. Percibe la calidez que genera en ambos."
        ],
        "emociones": ["tristeza"],
        "actividad": "ayudar"
    },
    {
        "titulo": "Videollamada de Café Virtual",
        "descripcion": "El contacto visual en directo fortalece los vínculos afectivos.",
        "tipo": "social",
        "consejo_rapido": "Tómate una bebida caliente compartiendo pantalla 5 minutos.",
        "duracion": "5 min",
        "pasos": [
            "1. Propón a un amigo conectar por video 5 minutos.",
            "2. Sostén tu taza compartiendo sonrisas frente a la cámara.",
            "3. Comenta anécdotas ligeras del día."
        ],
        "emociones": ["tristeza"],
        "actividad": "socializar"
    },
    {
        "titulo": "Compartir una Foto o Recuerdo Bonito",
        "descripcion": "Revive vivencias positivas compartiendo imágenes pasadas.",
        "tipo": "social",
        "consejo_rapido": "Manda una foto antigua al grupo de amigos recordando un gran momento.",
        "duracion": "3 min",
        "pasos": [
            "1. Busca en tu galería un recuerdo alegre con amigos o familia.",
            "2. Envíalo al grupo escribiendo: '¡Qué gran momento pasamos aquí!'",
            "3. Disfruta los comentarios y nostalgia positiva."
        ],
        "emociones": ["tristeza"],
        "actividad": "socializar"
    },
    {
        "titulo": "Saludar al Entorno Cercano",
        "descripcion": "Las interacciones breves cotidianas aportan sentido de pertenencia comunitaria.",
        "tipo": "social",
        "consejo_rapido": "Sonríe y saluda amablemente a un vecino o tendero.",
        "duracion": "2 min",
        "pasos": [
            "1. Al salir a la calle o al pasillo, cruza mirada y sonríe.",
            "2. Dedica un '¡Buenos días!' o '¡Hasta luego!' cercano.",
            "3. Nota el micro-contacto humano."
        ],
        "emociones": ["tristeza"],
        "actividad": "socializar"
    },
    {
        "titulo": "Planificar un Encuentro Futuro",
        "descripcion": "Anticipar actividades compartidas genera ilusión y reduce la melancolía.",
        "tipo": "social",
        "consejo_rapido": "Propón un plan sencillo en el calendario para el fin de semana.",
        "duracion": "4 min",
        "pasos": [
            "1. Escribe a un amigo proponiendo tomar un café o dar un paseo.",
            "2. Acuerden el día y la hora aproximada.",
            "3. Anota la fecha con entusiasmo."
        ],
        "emociones": ["tristeza"],
        "actividad": "planificar"
    },
    {
        "titulo": "Enviar una Nota de Voz Cálida",
        "descripcion": "La calidez de la voz transmite afecto más que el texto rígido.",
        "tipo": "social",
        "consejo_rapido": "Graba un audio de 30s enviando un saludo afectuoso.",
        "duracion": "2 min",
        "pasos": [
            "1. Presiona grabar en tu chat con una persona especial.",
            "2. Exprésale tu cariño y deséale un bonito día.",
            "3. Envíalo con espontaneidad."
        ],
        "emociones": ["tristeza"],
        "actividad": "llamar_ser_querido"
    },
    {
        "titulo": "Participación en Comunidad de Interés",
        "descripcion": "Comparte tus aficiones con personas apasionadas por lo mismo.",
        "tipo": "social",
        "consejo_rapido": "Comenta en un foro o grupo sobre tu libro, deporte o afición.",
        "duracion": "5 min",
        "pasos": [
            "1. Entra a tu grupo o foro de aficiones preferido.",
            "2. Comenta una publicación aportando tu visión respetuosa.",
            "3. Siéntete parte de un colectivo con tus mismos intereses."
        ],
        "emociones": ["tristeza"],
        "actividad": "socializar"
    },

    # 🟡 REFLEXIÓN Y EXPRESIÓN (Tristeza, Melancolía, Confusión)
    {
        "titulo": "Escritura Emocional Libre",
        "descripcion": "Plasma en papel tus pensamientos para darles estructura fuera de tu cabeza.",
        "tipo": "reflexion",
        "consejo_rapido": "Escribe durante 3 minutos sin juzgar ni corregir la gramática.",
        "duracion": "5 min",
        "pasos": [
            "1. Toma libreta y bolígrafo.",
            "2. Responde a: ¿Qué estoy sintiendo exactamente ahora mismo?",
            "3. Escribe todo sin pausar durante 3 minutos.",
            "4. Lee lo escrito y cierra la libreta sintiendo el desahogo."
        ],
        "emociones": ["tristeza", "miedo"],
        "actividad": "escribir"
    },
    {
        "titulo": "Registro de 3 Momentos Positivos",
        "descripcion": "Entrena tu foco de atención para valorar pequeños detalles del día.",
        "tipo": "reflexion",
        "consejo_rapido": "Anota 3 cosas buenas que te hayan ocurrido hoy.",
        "duracion": "3 min",
        "pasos": [
            "1. Identifica 3 sucesos agradables de las últimas horas.",
            "2. Escríbelos detallando brevemente por qué salieron bien.",
            "3. Siente gratitud por cada uno."
        ],
        "emociones": ["tristeza", "felicidad"],
        "actividad": "escribir"
    },
    {
        "titulo": "Nota de Auto-compasión",
        "descripcion": "Háblate con el mismo respeto y cariño que brindarías a tu mejor amigo.",
        "tipo": "reflexion",
        "consejo_rapido": "Redacta 3 frases recordándote que está bien cometer errores.",
        "duracion": "5 min",
        "pasos": [
            "1. Piensa en la situación que te preocupa o entristece.",
            "2. Escribe una frase comprensiva hacia ti mismo.",
            "3. Acepta que tus límites son humanos y mereces comprensión."
        ],
        "emociones": ["tristeza"],
        "actividad": "escribir"
    },
    {
        "titulo": "Escucha de Música Validante",
        "descripcion": "Permítete sentir la emoción de la melodía para procesarla sin resistencia.",
        "tipo": "reflexion",
        "consejo_rapido": "Escucha una melodía pausada cerrando los ojos.",
        "duracion": "4 min",
        "pasos": [
            "1. Elige una pieza musical tranquila o acústica.",
            "2. Cierra los ojos y atiende cada instrumento.",
            "3. Deja que la emoción fluya y se disipe gradualmente."
        ],
        "emociones": ["tristeza"],
        "actividad": "leer"
    },
    {
        "titulo": "Vaciado Mental de Preocupaciones",
        "descripcion": "Clasifica tus inquietudes entre las que puedes controlar y las que no.",
        "tipo": "reflexion",
        "consejo_rapido": "Haz dos listas: Lo que depende de mí / Lo que no depende de mí.",
        "duracion": "5 min",
        "pasos": [
            "1. Apunta todas tus inquietudes en una lista en blanco.",
            "2. Divide una hoja en dos columnas: 'Controlable' y 'No controlable'.",
            "3. Enfoca tu energía solo en el primer paso de la columna controlable."
        ],
        "emociones": ["miedo", "tristeza"],
        "actividad": "escribir"
    },
    {
        "titulo": "Lectura de 5 Páginas Inspiradoras",
        "descripcion": "Alimenta tu mente con nuevas perspectivas de lecturas valiosas.",
        "tipo": "reflexion",
        "consejo_rapido": "Lee 5 páginas de tu libro favorito o un artículo interesante.",
        "duracion": "5 min",
        "pasos": [
            "1. Abre un libro o artículo sobre crecimiento personal o ficción.",
            "2. Lee atentamente concentrándote en el contenido.",
            "3. Subraya una frase inspiradora."
        ],
        "emociones": ["tristeza"],
        "actividad": "leer"
    },
    {
        "titulo": "Fotografía de un Detalle del Entorno",
        "descripcion": "Ejercita la observación apreciativa fotografiando un detalle sutil.",
        "tipo": "reflexion",
        "consejo_rapido": "Captura una imagen bonita de la luz, una planta o una textura.",
        "duracion": "3 min",
        "pasos": [
            "1. Observa a tu alrededor buscando un ángulo o detalle atractivo.",
            "2. Toma una foto con tu cámara cuidando el encuadre.",
            "3. Observa el resultado apreciando la belleza sencilla."
        ],
        "emociones": ["felicidad", "sorpresa"],
        "actividad": "fotografiar"
    },
    {
        "titulo": "Boceto Creativo sin Juicio",
        "descripcion": "Expresa estados internos mediante garabatos o formas sin pretensión artística.",
        "tipo": "reflexion",
        "consejo_rapido": "Dibuja formas o trazos libres sobre papel durante 5 minutos.",
        "duracion": "5 min",
        "pasos": [
            "1. Toma papel y lápices de colores o bolígrafo.",
            "2. Deja deslizar la mano creando trazos según tu estado de ánimo.",
            "3. Observa las formas creadas como liberación simbólica."
        ],
        "emociones": ["tristeza", "ira"],
        "actividad": "pintar"
    },
    {
        "titulo": "Revisión de Logros Pasados",
        "descripcion": "Recuerda tu capacidad de superación mirando metas alcanzadas.",
        "tipo": "reflexion",
        "consejo_rapido": "Abre tu panel de logros o recuerdos para validar tus progresos.",
        "duracion": "4 min",
        "pasos": [
            "1. Accede a tus insignias o fotos de momentos de superación.",
            "2. Recuerda el esfuerzo que te costó cada avance.",
            "3. Reafirma tu confianza personal."
        ],
        "emociones": ["tristeza"],
        "actividad": "fotografiar"
    },
    {
        "titulo": "Alineación de Valores Personales",
        "descripcion": "Verifica si tus acciones recientes concuerdan con lo que más valoras.",
        "tipo": "reflexion",
        "consejo_rapido": "Pregúntate: ¿Mi comportamiento de hoy responde a mis prioridades?",
        "duracion": "4 min",
        "pasos": [
            "1. Escoge un valor central (ej. paz, amistad, superación).",
            "2. Reflexiona sobre tus elecciones de las últimas 24 horas.",
            "3. Diseña una pequeña corrección de rumbo si lo necesitas."
        ],
        "emociones": ["tristeza"],
        "actividad": "escribir"
    },

    # 🟣 SALUD MENTAL Y HÁBITOS (Orden, Rutina, Estrés General, Felicidad)
    {
        "titulo": "Orden Exprés del Escritorio",
        "descripcion": "El orden visual externo favorece la serenidad interna.",
        "tipo": "salud_mental",
        "consejo_rapido": "Ordena un espacio pequeño despejando papeles y objetos.",
        "duracion": "5 min",
        "pasos": [
            "1. Elige una mesa o superficie desordenada.",
            "2. Tira papeles inútiles y coloca cada objeto en su sitio.",
            "3. Disfruta de la sensación de claridad mental resultante."
        ],
        "emociones": ["miedo", "disgusto"],
        "actividad": "limpieza"
    },
    {
        "titulo": "Organización de las 3 Prioridades de Mañana",
        "descripcion": "Elimina la incertidumbre nocturna definiendo tus objetivos del día siguiente.",
        "tipo": "salud_mental",
        "consejo_rapido": "Anota las 3 tareas imprescindibles para mañana.",
        "duracion": "4 min",
        "pasos": [
            "1. Revisa tus pendientes pendientes.",
            "2. Escoge sólo las 3 tareas verdaderamente importantes.",
            "3. Cierra la agenda sabiendo exactamente por dónde empezar."
        ],
        "emociones": ["miedo"],
        "actividad": "planificar"
    },
    {
        "titulo": "Vaso de Agua e Hidratación Consciente",
        "descripcion": "La hidratación adecuada influye directamente en el cansancio y el humor.",
        "tipo": "salud_mental",
        "consejo_rapido": "Bébete un vaso grande de agua despacio.",
        "duracion": "1 min",
        "pasos": [
            "1. Llena un vaso de agua fresca.",
            "2. Bebe a sorbos lentos sintiendo cómo te revitalizas.",
            "3. Nota el refrescante alivio en tu organismo."
        ],
        "emociones": ["disgusto"],
        "actividad": "descansar"
    },
    {
        "titulo": "Ventilación y Renovación de Aire",
        "descripcion": "Renueva el oxígeno de tu habitación para refrescar el ambiente cargado.",
        "tipo": "salud_mental",
        "consejo_rapido": "Abre las ventanas 5 minutos para renovar el ambiente.",
        "duracion": "2 min",
        "pasos": [
            "1. Abre de par en par la ventana de tu estancia.",
            "2. Respira hondo sintiendo la corriente de aire limpio.",
            "3. Cierra apreciando la nitidez del espacio."
        ],
        "emociones": ["disgusto"],
        "actividad": "limpieza"
    },
    {
        "titulo": "Celebración de un Avance Diario",
        "descripcion": "Reconocer progresos impulsa el circuito de recompensa del cerebro.",
        "tipo": "salud_mental",
        "consejo_rapido": "Felicítate por haber completado una tarea pendiente.",
        "duracion": "2 min",
        "pasos": [
            "1. Piensa en un objetivo completado hoy.",
            "2. Di en voz alta: '¡Buen trabajo!'",
            "3. Disfruta la sensación de deber cumplido."
        ],
        "emociones": ["felicidad"],
        "actividad": "estudiar"
    },
    {
        "titulo": "Cuidado de Plantas y Espacios Verdes",
        "descripcion": "Atender seres vivos aporta calma y ritmo natural.",
        "tipo": "salud_mental",
        "consejo_rapido": "Riega y limpia las hojas de tus plantas.",
        "duracion": "4 min",
        "pasos": [
            "1. Revisa tus plantas en casa o balcón.",
            "2. Riega las que lo necesiten con cuidado.",
            "3. Retira hojas secas appreciando su verdor."
        ],
        "emociones": ["felicidad"],
        "actividad": "jardinería"
    },
    {
        "titulo": "Limpieza de Bandeja Digital",
        "descripcion": "El desorden digital en e-mails o descargas genera estrés subconsciente.",
        "tipo": "salud_mental",
        "consejo_rapido": "Borra 20 archivos o correos inútiles de tu dispositivo.",
        "duracion": "5 min",
        "pasos": [
            "1. Abre la carpeta de descargas o el correo entrante.",
            "2. Elimina 20 correos obsoletos.",
            "3. Vacía la papelera digital."
        ],
        "emociones": ["miedo"],
        "actividad": "limpieza"
    },
    {
        "titulo": "Bloqueo de Tiempo para Descanso",
        "descripcion": "Garantiza momentos de recarga en tu agenda sin remordimientos.",
        "tipo": "salud_mental",
        "consejo_rapido": "Reserva 30 minutos de tiempo libre intencional hoy.",
        "duracion": "5 min",
        "pasos": [
            "1. Mira tu plan para hoy o mañana.",
            "2. Bloquea 30 minutos sin tareas ni compromisos.",
            "3. Respeta ese espacio como sagrado."
        ],
        "emociones": ["disgusto"],
        "actividad": "planificar"
    },
    {
        "titulo": "Aprender una Curiosidad Nueva",
        "descripcion": "Estimula la plasticidad cerebral buscando un dato interesante.",
        "tipo": "salud_mental",
        "consejo_rapido": "Investiga durante 3 minutos un tema que te llame la atención.",
        "duracion": "4 min",
        "pasos": [
            "1. Busca un tema científico, histórico o artístico curioso.",
            "2. Lee un párrafo explicativo.",
            "3. Comparte el aprendizaje con alguien."
        ],
        "emociones": ["felicidad", "sorpresa"],
        "actividad": "estudiar"
    },
    {
        "titulo": "Ritual de Cierre de Jornada",
        "descripcion": "Desconecta del trabajo al finalizar para proteger tu salud mental.",
        "tipo": "salud_mental",
        "consejo_rapido": "Cierra aplicaciones de trabajo y di: 'Por hoy he terminado'.",
        "duracion": "3 min",
        "pasos": [
            "1. Guarda archivos y cierra pestañas de trabajo.",
            "2. Di verbalmente: 'Jornada completada con éxito'.",
            "3. Transiciona a tu tiempo personal."
        ],
        "emociones": ["felicidad", "disgusto"],
        "actividad": "planificar"
    }
]

class Command(BaseCommand):
    help = "Carga el catálogo inicial modular de 50 recomendaciones personalizadas."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Iniciando carga del catálogo de 50 recomendaciones..."))
        
        creadas = 0
        actualizadas = 0

        for data in RECOMENDACIONES_DATA:
            # 1. Buscar actividad sugerida si existe
            actividad_obj = None
            if data.get("actividad"):
                actividad_obj = Actividad.objects.filter(nombre__iexact=data["actividad"]).first()

            # 2. Crear o actualizar la recomendación por título
            rec, created = Recomendacion.objects.get_or_create(
                titulo=data["titulo"],
                defaults={
                    "descripcion": data["descripcion"],
                    "tipo": data["tipo"],
                    "consejo_rapido": data["consejo_rapido"],
                    "duracion": data["duracion"],
                    "pasos": data["pasos"],
                    "actividad_sugerida": actividad_obj
                }
            )

            if not created:
                rec.descripcion = data["descripcion"]
                rec.tipo = data["tipo"]
                rec.consejo_rapido = data["consejo_rapido"]
                rec.duracion = data["duracion"]
                rec.pasos = data["pasos"]
                rec.actividad_sugerida = actividad_obj
                rec.save()
                actualizadas += 1
            else:
                creadas += 1

            # 3. Asociar emociones desencadenantes
            for emo_nombre in data.get("emociones", []):
                emocion_obj = Emocion.objects.filter(nombre__iexact=emo_nombre).first()
                if emocion_obj:
                    RecomendacionEmocion.objects.get_or_create(
                        recomendacion=rec,
                        emocion=emocion_obj
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"[OK] Carga completada con exito: {creadas} recomendaciones creadas, {actualizadas} actualizadas."
            )
        )
