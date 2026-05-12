# Smart Expert Mental Health Support — Backend

Django + GraphQL backend for the Smart Expert Mental Health Support mobile application.

## Tech Stack

- **Django 5.1** — Web framework
- **Graphene-Django** — GraphQL API
- **Django Channels** — WebSocket support
- **Django REST Framework** — REST endpoints for file uploads
- **SQLite** (dev) / **PostgreSQL** (production)

## Quick Start

```bash
# 1. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment variables
cp .env.example .env
# Edit .env with your values

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver 0.0.0.0:8000
```

## Environment Variables

See `.env.example` for all required variables. Key ones:

| Variable | Description | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | insecure dev key |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `*` |
| `DATABASE_URL` | PostgreSQL URL (optional) | SQLite |
| `MAILTRAP_API_TOKEN` | Email delivery token | console backend |
| `FRONTEND_URL` | Mobile app deep link base | `http://localhost:8081` |

## API Endpoints

| Endpoint | Description |
|---|---|
| `/graphql/` | GraphQL API (GraphiQL enabled in DEBUG) |
| `/api/upload-profile-picture/` | Profile picture upload (JWT required) |
| `/api/profile-picture/` | Get profile picture URL (JWT required) |
| `/admin/` | Django admin panel |

## Project Structure

```
backend/
├── healthbackend/     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── core/              # Main application
│   ├── models.py      # User, Therapist, SecurityQuestion, etc.
│   ├── schema.py      # GraphQL schema & mutations
│   ├── api_views.py   # REST API views
│   ├── signals.py     # Password reset email signal
│   └── consumers.py   # WebSocket consumers
├── project_templates/ # Email & HTML templates
└── requirements.txt
```
