# FlowForge Backend (Django)

This is the backend component of FlowForge, built with Django.

## Features
- RESTful API for workflow management
- Natural Language Processing (NL Parsing) using free providers (Groq or NVIDIA NIM)
- Workflow execution engine (stubbed)
- Credential management for external services
- Database models for workflows and credentials

## API Endpoints
- `POST /api/workflows/parse` - Parse natural language request into structured workflow JSON
- `GET /api/workflows` - List all workflows
- `POST /api/workflows` - Create a new workflow
- `GET /api/workflows/<id>` - Retrieve a specific workflow
- `POST /api/workflows/<id>/run` - Execute a workflow (stubbed)

## Project Structure
```
.
├── manage.py
├── flowforge_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── workflows/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── services/
│       ├── __init__.py
│       ├── nl_parser.py
│       └── execution_engine.py
�└── BACKEND_README.md
```

## Setup Instructions

1. **Checkout the backend branch** (if you haven't already):
   ```bash
   git checkout backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: We'll create a requirements.txt file next.*

4. **Create a requirements.txt file** (if not present) with the following content:
   ```
   Django==4.2.0
   ```

5. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser** (for Django admin):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`.

## Environment Variables
Create a `.env` file in the root directory (copy from `.env.example` if provided) and set:
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: Set to `False` in production
   - `ALLOWED_HOSTS`: Comma-separated list of hosts
   - `DATABASE_URL`: Default is SQLite, but can be changed to PostgreSQL, etc.

## NL Parser Configuration
The NL parser service is currently stubbed. To integrate with a free LLM provider:
1. Sign up for an API key from Groq (https://groq.com) or NVIDIA NIM.
2. Add the API key to your `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```
   or
   ```
   NVIDIA_NIM_API_KEY=your_nvidia_nim_api_key
   ```
3. Update the `workflows/services/nl_parser.py` file to use the actual API.

## Workflow Execution
The execution engine is currently stubbed. To implement actual execution:
1. Update `workflows/services/execution_engine.py` to perform the desired actions.
2. Consider using asynchronous task queues (like Celery) for long-running workflows.

## Testing
Run the Django test suite:
```bash
python manage.py test
```

## Deployment
For production, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx, Apache)
- Using a managed database (PostgreSQL, MySQL)
- Setting up environment variables securely

## License
This project is part of FlowForge and is licensed under the MIT License.
