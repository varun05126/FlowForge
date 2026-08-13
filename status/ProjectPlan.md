# FlowForge Project Plan and Status

This file tracks the progress of the FlowForge project across its phases.

## Current Status (as of 2026-08-13)

### Phase 1: Project Setup and Scaffolding - **COMPLETED**
- [x] Repository initialized with LICENSE (MIT)
- [x] Created three branches: `main`, `frontend`, `backend`
- [x] Set up `main` branch with:
    - [x] Comprehensive README.md (this file's counterpart)
    - [x] Architecture diagram (`docs/architecture.svg`)
    - [x] Flow diagram (`docs/flow.svg`)
    - [x] .gitignore for Node.js/Python/Django
- [x] Set up `frontend` branch (HTML/CSS/JS):
    - [x] Basic workflow builder UI (index.html, styles.css, app.js)
    - [x] Frontend-specific README.md
- [x] Set up `backend` branch (Django):
    - [x] Django project structure
    - [x] Workflows app with models (Workflow, Credential)
    - [x] Stubbed services for NL parser and execution engine
    - [x] REST API views for workflow CRUD, parsing, and execution
    - [x] Backend-specific README (BACKEND_README.md)
- [x] Pushed all three branches to origin

### Phase 2: Core Functionality Implementation - **NOT STARTED**
- [ ] Frontend: Connect to backend API for parsing and saving workflows
- [ ] Backend: Implement actual NL parsing using Groq or NVIDIA NIM API
- [ ] Backend: Implement workflow execution engine to run scheduled/triggered workflows
- [ ] Backend: Implement credential vault (encrypted storage for API keys/secrets)
- [ ] Frontend: Display workflow list, detail views, and run history

### Phase 3: Integration and Advanced Features - **NOT STARTED**
- [ ] Frontend: Workflow visualizer (node-based or flowchart)
- [ ] Backend: Support for various triggers (schedule, webhook, manual)
- [ ] Backend: Integration with external services (ERP, WhatsApp/Telegram/Email/SMS, webhooks)
- [ ] Backend: Add authentication and authorization (JWT)
- [ ] Frontend: User authentication and personal workflow management

### Phase 4: Testing, Deployment, and Documentation - **NOT STARTED**
- [ ] Writing unit and integration tests
- [ ] Setting up CI/CD pipeline
- [ ] Dockerizing the application
- [ ] Comprehensive user and developer documentation
- [ ] Performance optimization and security audits

## Notes
- The NL parser and execution engine are currently stubbed in the backend.
- The frontend is a static HTML/CSS/JS app that simulates parsing.
- Future work will focus on implementing the stubbed components and connecting the frontend to the backend.

## Next Immediate Steps
1. Choose a branch to work on (frontend or backend) to begin Phase 2.
2. For backend: 
   - Install dependencies (Django, requests for API calls to Groq/NVIDIA)
   - Implement the actual NL parser service to call a free LLM API.
   - Implement the execution engine to perform actual workflow steps.
3. For frontend:
   - Modify app.js to make actual API calls to the backend.
   - Add components for workflow list and detail views.

## References
- [Main README](./README.md)
- [Backend README](./BACKEND_README.md) (in backend branch)
- [Frontend README](./FRONTEND_README.md) (in frontend branch)
- Architecture: [docs/architecture.svg](./docs/architecture.svg)
- Flow: [docs/flow.svg](./docs/flow.svg)
