# Sitio "Dockerize" — Django + PostgreSQL + Docker

Explica qué es Docker. Separación estricta: **frontend = diseño**, **backend = lógica**.

## Con Docker (recomendado)

```powershell
docker compose up --build
```

Y listo: http://127.0.0.1:8000

El entrypoint espera a PostgreSQL, aplica migraciones y carga los datos iniciales.
PostgreSQL queda publicado en el puerto **5432**.

| Servicio | URL | Notas |
|---|---|---|
| web | http://127.0.0.1:8000 | Django tras Gunicorn |
| db | 127.0.0.1:5432 | PostgreSQL 16, usuario `dockerize`, volumen `db_data` |
| adminer | http://127.0.0.1:8082 | solo con `docker compose --profile tools up` |

### Otros comandos

```powershell
docker compose up -d --build              # segundo plano
docker compose logs -f web                # ver logs
docker compose ps                         # estado + healthchecks
docker compose exec web python manage.py shell
docker compose exec db psql -U dockerize -d docker_basico
docker compose down                       # parar (conserva los datos)
docker compose down -v                    # parar y BORRAR el volumen de PostgreSQL
```

### Modo producción (Gunicorn + DEBUG=False)

```powershell
Copy-Item .env.example .env   # define DJANGO_SECRET_KEY antes de seguir
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Sirve los estáticos con WhiteNoise (`base.<hash>.css`) y deja de publicar el
puerto de la base de datos. Requiere `DJANGO_SECRET_KEY` en el `.env` de la raíz:
con `DEBUG=False` el proyecto se niega a arrancar usando la clave de ejemplo.

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

## Sin Docker (SQLite o PostgreSQL local)

```powershell
cd backend
pip install -r requirements.txt

# Sin variables de entorno el proyecto usa SQLite (backend/db.sqlite3).
python manage.py migrate
python manage.py cargar_datos       # planes + equipo
python manage.py runserver
```

Para usar un PostgreSQL local en vez de SQLite, define `DATABASE_URL`:

```powershell
$env:DATABASE_URL = "postgres://dockerize:dockerize@127.0.0.1:5432/docker_basico"
python manage.py crear_base_datos   # crea la BD en PostgreSQL si no existe
python manage.py migrate
```

## Estructura

```
proyecto basico/
├── Dockerfile                 # build multi-stage, usuario no root
├── docker-compose.yml         # db + web (+ adminer en perfil "tools")
├── docker-compose.prod.yml    # override para producción
├── entrypoint.sh              # espera PostgreSQL, migrate, collectstatic, gunicorn
├── .gitattributes             # fuerza LF en .sh (si no, el shebang se rompe)
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

## La base de datos

El camino portable, el que usan Docker y Render, es siempre el mismo:

```powershell
python manage.py migrate --noinput   # crea las 15 tablas
python manage.py cargar_datos        # 3 planes, 17 características, 4 integrantes
```

`migrate` + `cargar_datos` no dependen del motor, así que funcionan igual en
SQLite, en el PostgreSQL de `docker-compose` y en el de Render.

### `dockerfile_basico.sql` (dialecto MySQL, solo histórico)

Este archivo se generó cuando el proyecto usaba MySQL 8 y **no es compatible con
PostgreSQL**: usa backticks, `ENGINE=InnoDB`, `CHARACTER SET utf8mb4` y
`mysqldump`. Se conserva como referencia del diseño original de los datos, no
como fuente de verdad. No lo uses contra PostgreSQL.

Para obtener el equivalente en PostgreSQL:

```powershell
# estructura + datos, en un solo archivo
docker compose exec -T db pg_dump -U dockerize -d docker_basico > dump_postgres.sql

# importarlo en un PostgreSQL vacío
docker compose exec -T db psql -U dockerize -d docker_basico < dump_postgres.sql
```

En Render nunca se importa SQL: la base la crea el proveedor y el entrypoint solo
ejecuta `migrate`.

## Detalles del dockerizado
- **Multi-stage**: `psycopg[binary]` y `dj-database-url` se instalan desde ruedas
  ya compiladas, así que la imagen no necesita compilador ni cliente de MySQL.
- **Usuario no root**: la app corre como `appuser` (uid 1000).
- **Sin secretos en la imagen**: `.dockerignore` excluye `.env` y `.git`; las
  credenciales se inyectan por `env_file`/`environment` en tiempo de ejecución.
- **Healthchecks**: PostgreSQL usa `pg_isready`; el web hace un GET a `/` sobre el
  puerto que indique `$PORT`. `depends_on: condition: service_healthy` garantiza
  que Django no arranque antes que la base.
- **Persistencia**: volumen nombrado `db_data`; los datos sobreviven a `down`.
- **Puerto**: Gunicorn escucha en `0.0.0.0:${PORT:-8000}`. Render inyecta `PORT`
  (10000 por defecto en el plan gratuito), por eso nada está fijado a mano.

## Configuración

Todo sale de variables de entorno. `backend/config/conf.py` las resuelve y
`settings.py` solo las expone con los nombres que Django espera.

| Variable | Para qué | Valor en producción |
|---|---|---|
| `DATABASE_URL` | DSN de PostgreSQL | **obligatoria** (Internal Database URL de Render) |
| `DJANGO_SECRET_KEY` | clave de Django | **obligatoria**, generada al azar |
| `DJANGO_DEBUG` | modo depuración | `False` |
| `RENDER_EXTERNAL_HOSTNAME` | dominio público | la define Render, no hay que crearla |
| `DJANGO_ALLOWED_HOSTS` | hosts extra | solo si usas dominio propio |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | orígenes CSRF | solo si usas dominio propio |
| `DB_CONN_MAX_AGE` | reutilizar conexiones | `600` |
| `GUNICORN_WORKERS` | workers de Gunicorn | `3` |
| `PORT` | puerto del servidor | lo define Render |

Si no hay `DATABASE_URL`, el proyecto usa variables sueltas
(`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`). Si tampoco hay
ninguna, cae a SQLite para que `manage.py` siga siendo usable.

`RENDER_EXTERNAL_HOSTNAME` alcanza porque Render la inyecta sola: el proyecto la
añade automáticamente a `ALLOWED_HOSTS` y a `CSRF_TRUSTED_ORIGINS` como
`https://<hostname>`.

## Despliegue en Render

1. Crea la base: **New > Postgres**, y cópiala el **Internal Database URL**.
2. Crea el servicio: **New > Web Service**, Connect repo, Runtime **Docker**.
3. Variables de entorno del Web Service:

   | Clave | Valor |
   |---|---|
   | `DATABASE_URL` | el Internal Database URL de tu Postgres |
   | `DJANGO_SECRET_KEY` | `python -c "import secrets; print(secrets.token_urlsafe(64))"` |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_TRUST_X_FORWARDED_PROTO` | `1` |
   | `DJANGO_SECURE_SSL_REDIRECT` | `1` |

   No definas `PORT` ni `RENDER_EXTERNAL_HOSTNAME`: los provee Render.
4. El entrypoint se encarga del resto: espera la base, `migrate --noinput`,
   `collectstatic --noinput` y arranca Gunicorn.
5. El plan gratuito apaga el servicio tras 15 min de inactividad y **borra el
   disco en cada despliegue**, por eso `collectstatic` corre en cada arranque.

La configuración base de datos de PostgreSQL **no** va en Render: la inyecta el
propensor de la base, y Django solo lee `DATABASE_URL`.

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
