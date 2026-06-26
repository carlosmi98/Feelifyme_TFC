# Feelifyme — Registro y Visualización Emocional

**Feelifyme** es una aplicación web de bienestar emocional desarrollada como Trabajo de Fin de Ciclo (TFC). Permite a los usuarios registrar cómo se sienten día a día a través de una rueda de emociones interactiva y un calendario visual, fomentando el autoconocimiento y la inteligencia emocional.

> 📄 **Archivo de copia de seguridad (fixture):** [`backend/feelifyme_backup.json`](./backend/feelifyme_backup.json)

---

## Tecnologías utilizadas

### Frontend

| Tecnología | Versión | Descripción |
|---|---|---|
| **React** | 19 | Framework de UI |
| **Vite** | 5 | Bundler y servidor de desarrollo |
| **React Router DOM** | 7 | Enrutamiento cliente-side con rutas públicas y privadas |
| **ECharts for React** | 3 | Gráficos interactivos (Sunburst, Pie, Bar) |
| **Axios** | 1 | Cliente HTTP para comunicación con la API Django |
| **CSS Vanilla** | — | Estilos con variables CSS y Media Queries responsive |

### Backend

| Tecnología | Versión | Descripción |
|---|---|---|
| **Python** | 3.12+ | Lenguaje del servidor |
| **Django** | 6.0.3 | Framework web y ORM |
| **Django REST Framework** | 3.16 | Construcción de la API REST |
| **djangorestframework-simplejwt** | 5.5 | Autenticación con tokens JWT (access + refresh) |
| **django-cors-headers** | 4.9 | Gestión de peticiones CORS desde el frontend |
| **PostgreSQL** | 15+ | Base de datos relacional para persistencia de datos |

---

## Estructura del proyecto

```
feelifyme/
├── backend/                          # Servidor Django
│   ├── backend/                      # Configuración Django (settings, urls, wsgi)
│   │   ├── settings.py
│   │   └── urls.py
│   ├── backFeelifyme/                # App principal
│   │   ├── models.py                 # Modelos: Emocion, Actividad, RegistroDiario...
│   │   ├── views.py                  # Vistas API REST
│   │   ├── serializers.py            # Serialización de datos
│   │   ├── urls.py                   # Rutas de la API
│   │   └── migrations/               # Migraciones de la base de datos
│   ├── manage.py
│   └── requirements.txt              # Dependencias Python
│
└── frontend/                         # Cliente React + Vite
    ├── src/
    │   ├── App.jsx                   # Enrutamiento principal (público / privado)
    │   ├── layouts/
    │   │   ├── LayoutApp.jsx         # Raíz: gestiona estado de sesión global
    │   │   ├── PublicLayout.jsx      # Layout páginas públicas
    │   │   └── PrivateLayout.jsx     # Layout con guardia de autenticación
    │   └── pages/
    │       ├── public/               # Inicio, Login, Registro, Sobre nosotros
    │       └── private/
    │           ├── MisEmociones/     # Calendario mensual
    │           ├── RegistroEmocion/  # Registro diario con la Rueda Sunburst
    │           └── mi_evolucion/     # Dashboard de estadísticas mensuales
    ├── package.json
    └── vite.config.js
```

---

## Requisitos previos

Asegúrate de tener instalado lo siguiente antes de comenzar:

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| **Python** | 3.11+ | https://www.python.org/downloads/ |
| **Node.js** | 18+ | https://nodejs.org/ |
| **Git** | Cualquiera | https://git-scm.com/ |

> **Comprobación rápida:** Abre una terminal y ejecuta `python --version`, `node --version` y `git --version` para verificar que están instalados correctamente.

---

## Instalación y puesta en marcha

### 1. Clonar el repositorio

```bash
git clone https://github.com/CarlosM98/feelifyme.git
cd feelifyme
```

---

### 2. Configurar el Backend (Django)

Abre una terminal y navega al directorio del backend:

```bash
cd backend
```

#### 2.1 Crear y activar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en macOS / Linux
source venv/bin/activate
```

> Sabrás que el entorno está activo porque verás `(venv)` al inicio de la línea de comandos.

#### 2.2 Instalar las dependencias Python

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar e importar la base de datos

El proyecto utiliza **PostgreSQL**. Sigue estos pasos para configurarlo:

1. Crea una base de datos vacía en PostgreSQL (puedes llamarla `feelifyme`).
2. Configura las credenciales de conexión (usuario, contraseña, host y puerto) de tu base de datos local en la sección `DATABASES` del archivo `backend/backend/settings.py`.
3. Ejecuta las migraciones para crear la estructura de tablas:
   ```bash
   python manage.py migrate
   ```
4. El repositorio incluye el archivo **`backend/feelifyme_backup.json`** con toda la estructura y datos iniciales necesarios (catálogo de emociones, actividades, etc.). Restáuralos ejecutando:
   ```bash
   python -X utf8=1 manage.py loaddata feelifyme_backup.json
   ```

> ✅ Tras este paso la base de datos PostgreSQL contendrá todas las tablas y el catálogo completo de emociones y actividades.

#### 2.4 Usuario de prueba (Demo)

Para evaluar el proyecto con un historial completo de registros emocionales y ver los gráficos dinámicos del frontend funcionando al instante, puedes iniciar sesión con las siguientes credenciales:

* **Usuario/Email:** `julia@julia.com`
* **Contraseña:** `prueba123`

#### 2.5 (Opcional) Crear un superusuario para el panel de administración

```bash
python manage.py createsuperuser
```

Accesible en `http://localhost:8000/admin/` una vez arrancado el servidor.

#### 2.6 Arrancar el servidor Django

```bash
python manage.py runserver
```

✅ El backend estará disponible en **`http://localhost:8000`**

---

### 3. Configurar el Frontend (React + Vite)

Abre una **nueva terminal** (deja el backend corriendo) y navega al directorio del frontend:

```bash
cd frontend
```

#### 3.1 Instalar las dependencias Node

```bash
npm install
```

#### 3.2 Arrancar el servidor de desarrollo

```bash
npm run dev
```

✅ La aplicación estará disponible en **`http://localhost:5173`**

---

### Resumen rápido (instalación limpia)

```bash
# 1. Clonar
git clone https://github.com/CarlosM98/feelifyme.git && cd feelifyme

# 2. Backend
# (Recuerda haber creado primero la base de datos vacía en PostgreSQL y haber configurado settings.py)
cd backend
python -m venv venv
.\venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python -X utf8=1 manage.py loaddata feelifyme_backup.json
python manage.py runserver       # http://localhost:8000

# 3. Frontend (nueva terminal)
cd ../frontend
npm install
npm run dev                      # http://localhost:5173
```

---

## Base de datos

El proyecto usa **PostgreSQL** como base de datos para una mayor robustez y escalabilidad.

| Archivo / Componente | Descripción |
|---|---|
| `backend/feelifyme_backup.json` | Respaldo (fixture) completo con la estructura y datos del catálogo (emociones, actividades) y datos de prueba. **Incluido en el repositorio.** |
| `PostgreSQL (local)` | Base de datos relacional configurada en `settings.py`. |

- La estructura de tablas se crea automáticamente al ejecutar `python manage.py migrate`.
- Los datos y el catálogo inicial se restauran importando `feelifyme_backup.json` mediante el comando `python -X utf8=1 manage.py loaddata feelifyme_backup.json`.

### Modelos principales

| Modelo | Descripción |
|---|---|
| `Emocion` | Catálogo jerárquico de emociones (3 niveles: primaria → secundaria → terciaria) |
| `Actividad` | Catálogo de actividades disponibles para registrar |
| `RegistroDiario` | Registro de un usuario en una fecha concreta |
| `EmocionRegistrada` | Relación entre un registro diario y una emoción seleccionada |
| `ActividadRealizada` | Relación entre un registro diario y una actividad realizada |

---

## Endpoints de la API

Todos los endpoints tienen el prefijo `/api/`.

### Autenticación y usuarios

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/api/users/register/` | ❌ | Registro de nuevo usuario |
| `POST` | `/api/users/login/` | ❌ | Login → devuelve `access` y `refresh` JWT |
| `POST` | `/api/users/refresh/` | ❌ | Refresca el token de acceso |
| `GET` | `/api/users/me/` | ✅ | Obtiene los datos del usuario autenticado |
| `PUT` | `/api/users/me/` | ✅ | Actualiza los datos del usuario |
| `DELETE` | `/api/users/me/` | ✅ | Elimina la cuenta del usuario |

### Catálogo

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/emociones/arbol/` | ❌ | Árbol jerárquico de emociones (formato JSON para ECharts) |
| `GET` | `/api/actividades/` | ❌ | Lista de todas las actividades disponibles |

### Registro diario

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/api/registro-diario/` | ✅ | Crea un nuevo registro con emociones y actividades |
| `GET` | `/api/resumen-dia/?fecha=YYYY-MM-DD` | ✅ | Resumen cronológico de registros de un día |
| `PUT` | `/api/registros-edicion/<id>/` | ✅ | Edita un registro del día actual |
| `DELETE` | `/api/registros-edicion/<id>/` | ✅ | Borra un registro del día actual |

### Calendario y evolución

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/api/calendario/resumen/?mes=YYYY-MM` | ✅ | Resumen de emociones y actividades por día del mes |
| `GET` | `/api/evolucion/mensual/?mes=YYYY-MM` | ✅ | Conteo de emociones primarias y actividades del mes (para gráficos) |

> **Autenticación:** Los endpoints marcados con ✅ requieren el header `Authorization: Bearer <access_token>`.

---

## Funcionalidades principales

- **Autenticación con JWT:** Registro e inicio de sesión con tokens almacenados en `localStorage`. Las rutas privadas están protegidas mediante un guardia de rutas en React.
- **Calendario interactivo:** Visualización mensual con navegación entre meses, indicador del día actual y resumen de emociones y actividades por casilla.
- **Rueda de Emociones (Sunburst):** Gráfico interactivo con 3 niveles jerárquicos de emociones (primarias, secundarias y terciarias) usando ECharts.
- **Registro diario:** Posibilidad de registrar múltiples entradas al día, cada una con emociones, actividades y notas libres.
- **Dashboard de evolución:** Gráficos mensuales de distribución de emociones primarias (pie chart) y ranking de actividades más frecuentes (bar chart).
- **Diseño Responsive:** Adaptado para escritorio, tablet (768px) y móvil (480px).

---

## Solución de problemas frecuentes

| Problema | Solución |
|---|---|
| `ModuleNotFoundError` al arrancar Django | Asegúrate de tener el entorno virtual activado (`.\venv\Scripts\activate`) |
| La rueda de emociones aparece vacía | Ejecuta `python manage.py loaddata backFeelifyme/fixtures/emociones.json` |
| Error CORS en el frontend | Comprueba que el backend está corriendo en `localhost:8000` |
| `npm install` falla | Verifica que tienes Node.js 18+ con `node --version` |
| Puerto 8000 ocupado | Usa `python manage.py runserver 8001` y actualiza la URL base en el frontend |

---

## Mejoras futuras previstas

- [x] Migración de SQLite a **PostgreSQL**
- [ ] Cambio de `localStorage` a **HttpOnly Cookies** para mayor seguridad en los tokens
- [ ] **Internacionalización (i18n)** con `react-i18next`
- [ ] Integración de modelos de **Inteligencia Artificial** para sugerencias personalizadas
- [ ] Despliegue en producción con **Vercel** (frontend) y **Railway/Render** (backend)

---

## Autor

**Carlos M.** — Desarrollo Web · TFC 2025/2026
