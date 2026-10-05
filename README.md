# Sitio "Dockerize" — Django + MySQL + Docker

Explica qué es Docker. Separación estricta: **frontend = diseño**, **backend = lógica**.

## Con Docker (recomendado)

```powershell
docker compose up --build
```

Y listo: http://127.0.0.1:8000

El entrypoint espera a MySQL, aplica migraciones y carga los datos iniciales.
MySQL queda published en el puerto **3307** (el 3306 de tu máquina ya lo usa tu MySQL local).

| Servicio | URL | Notas |
|---|---|---|
| web | http://127.0.0.1:8000 | Django |
| db | 127.0.0.1:3307 | MySQL 8, usuario `dockerize`, volumen `db_data` |
| adminer | http://127.0.0.1:8082 | solo con `docker compose --profile tools up` |

### Otros comandos

```powershell
docker compose up -d --build              # segundo plano
docker compose logs -f web                # ver logs
docker compose ps                         # estado + healthchecks
docker compose exec web python manage.py shell
docker compose exec db mysql -udockerize -pdockerize docker_basico
docker compose down                       # parar (conserva los datos)
docker compose down -v                    # parar y BORRAR el volumen de MySQL
```

### Modo producción (Gunicorn + DEBUG=False)

```powershell
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Cambia a Gunicorn (3 workers), sirve los estáticos con WhiteNoise (`base.<hash>.css`)
y deja de publicar el puerto de MySQL.

### Crear el usuario admin dentro del contenedor

```powershell
docker compose run --rm -e DJANGO_SUPERUSER_PASSWORD='TuClave#2026' web admin --noinput --username admin --email admin@dockerize.dev
```

Panel: http://127.0.0.1:8000/admin/

### Ajustar puertos o credenciales

Copia `.env.example` a `.env` en la raíz (Compose lo lee automáticamente):

```powershell
Copy-Item .env.example .env
```

---

## Sin Docker (MySQL local)

```powershell
cd backend
pip install -r requirements.txt

python manage.py crear_base_datos   # crea la BD en MySQL si no existe
python manage.py migrate
python manage.py cargar_datos       # planes + equipo
python manage.py runserver
```

## Estructura

```
proyecto basico/
├── Dockerfile                 # build multi-stage, usuario no root
├── docker-compose.yml         # db + web (+ adminer en perfil "tools")
├── docker-compose.prod.yml    # override para producción
├── entrypoint.sh              # espera MySQL, migrate, collectstatic, arranca
├── .dockerignore              # excluye .env, .git, cachés y estáticos
├── .env.example               # variables de Compose
│
├── backend/                   # TODA la lógica (Django, POO)
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env                   # credenciales (no se versiona)
│   ├── config/                # proyecto
│   │   ├── conf.py            # configuración por clases (POO)
│   │   ├── settings.py        # expone conf.py con los nombres de Django
│   │   ├── urls.py            # URLs raíz + handlers 404/500
│   │   └── wsgi.py / asgi.py
│   └── apps/
│       ├── core/
│       │   ├── models/        # modelo = paquete, un archivo por dominio
│       │   │   ├── base.py    #   TimeStampedModel, PublishedModel
│       │   │   ├── plan.py    #   Plan, PlanFeature, PlanQuerySet
│       │   │   ├── team.py    #   TeamMember
│       │   │   └── contact.py #   ContactMessage
│       │   ├── services.py    # ★ lógica de negocio (clases de servicio)
│       │   ├── forms.py
│       │   ├── views.py       # ★ solo CBV
│       │   ├── urls.py
│       │   ├── admin.py
│       │   ├── context_processors.py
│       │   ├── templatetags/core_extras.py  # filtros (resaltado de código)
│       │   └── management/commands/         # crear_base_datos, cargar_datos
│       └── accounts/          # registro / login / perfil
│
└── frontend/                  # SOLO diseño
    ├── templates/
    │   ├── base.html          # ★ template raíz (navbar + footer + blocks)
    │   ├── index.html         # página inicial: qué es Docker
    │   ├── quienes_somos.html
    │   ├── precios.html
    │   ├── plan_detalle.html
    │   ├── 404.html / 500.html
    │   ├── auth/              # login, registro, perfil
    │   └── partials/icono.html
    └── static/
        ├── css/base.css       # ★ TODO el CSS en un solo archivo
        └── js/main.js         # solo interacciones (menú móvil)
```

## La base de datos en un solo archivo

`dockerfile_basico.sql` (en la raíz) contiene **toda** la base en un único archivo:

| Sección | Contenido |
|---|---|
| 1 | `CREATE DATABASE` + `USE` |
| 2 | Las 15 tablas (`CREATE TABLE`) |
| 3 | Los datos: 3 planes, 17 características, 4 integrantes, migraciones y permisos |

No incluye usuarios ni contraseñas. Tras importarlo, crea el primer admin con:

```powershell
python manage.py createsuperuser
```

**Importarlo**

```powershell
# línea de comandos
mysql -u root -p < dockerfile_basico.sql

# contra el MySQL de Docker
docker compose exec -T db mysql -uroot -proot < dockerfile_basico.sql
```

En phpMyAdmin: pestaña **Importar** → elige el archivo → **Continuar**.
En Workbench: **Schema** → clic derecho → **Import SQL Script**.

Si tu servidor ya tiene una base con otro nombre, edita las líneas
`CREATE DATABASE` y `USE` de la sección 1.

**Regenerarlo** desde tu MySQL local:

```powershell
mysqldump -uroot -proot --no-data docker_basico --result-file=_estructura.sql
mysqldump -uroot -proot --no-create-info --single-transaction --result-file=_datos.sql docker_basico core_plan core_planfeature core_teammember django_migrations django_content_type auth_permission
cmd /c "copy /b _cabecera.sql + _estructura.sql + _datos.sql dockerfile_basico.sql"
```

## Detalles del dockerizado
- **Multi-stage**: las herramientas de compilación de `mysqlclient` viven en la etapa
  `deps`; la imagen final solo lleva el venv y las librerías de MySQL.
- **Usuario no root**: la app corre como `appuser` (uid 1000).
- **Sin secretos en la imagen**: `.dockerignore` excluye `.env` y `.git`; las
  credenciales se inyectan por `env_file`/`environment` en tiempo de ejecución.
- **Healthchecks**: MySQL usa `mysqladmin ping`; el web hace un GET a `/`.
  `depends_on: condition: service_healthy` garantiza que Django no arranque antes.
- **Persistencia**: volumen nombrado `db_data`; los datos sobreviven a `down`.

## Configuración

`backend/.env` (usado sin Docker y como `env_file` en Compose):

```ini
DJANGO_SECRET_KEY=cambia-esta-clave-en-produccion
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,testserver

MYSQL_DATABASE=docker_basico
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Las variables reales del entorno tienen prioridad sobre el `.env`.
Dentro de Compose, `MYSQL_HOST` se sobrescribe a `db` (el nombre del servicio).

## Rutas

| Ruta | Vista | Descripción |
|---|---|---|
| `/` | `core.HomeView` | Inicio: qué es Docker |
| `/quienes-somos/` | `core.AboutView` | Nosotros, valores, equipo, hitos |
| `/precios/` | `core.PricingListView` | Planes desde la BD |
| `/precios/<slug>/` | `core.PlanDetailView` | Detalle de plan |
| `/contacto/` | `core.ContactView` | Recibe el formulario (POST) |
| `/cuentas/registro/` | `accounts.RegisterView` | Crea usuario + perfil e inicia sesión |
| `/cuentas/login/` | `accounts.LoginView` | Usuario **o** correo |
| `/cuentas/logout/` | `accounts.LogoutView` | POST |
| `/cuentas/perfil/` | `accounts.ProfileDetailView` | Requiere sesión |

## Notas de diseño

- **Colores**: escala azul `--azul-950` a `--azul-50` + blanco; texto `--texto: #0a1c3d`.
  Contraste alto (botón `--azul-700` `#0b4fd8` sobre blanco ≈ 7:1).
- **Estética programación**: monoespaciada, ventanas de terminal, resaltado de sintaxis
  con los filtros de `core_extras.py`, y grid de fondo en el hero.
- **Responsive**: menú hamburguesa bajo 820px (`main.js` solo añade/quita clases;
  todo el estilo está en `base.css`).
