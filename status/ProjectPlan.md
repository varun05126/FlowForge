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
    - [x] Rule-based NL parser service
    - [x] Simulated execution engine service
    - [x] Encrypted credential vault service
    - [x] REST API views for workflow CRUD, parsing, execution, and credential management
    - [x] Backend-specific README (BACKEND_README.md)
- [x] Pushed all three branches to origin

### Phase 2: Core Functionality Implementation - **COMPLETED**
- [x] Frontend: Connected to backend API for parsing and saving workflows
- [x] Backend: Implemented rule-based NL parser for extracting workflow components from natural language
- [x] Backend: Implemented simulated execution engine that runs workflows with realistic steps and mock data
- [x] Backend: Implemented credential vault with encryption for storing API keys and secrets
- [x] Backend: Added credential management endpoints (CRUD operations)
- [x] Frontend: Display workflow list, detail views, and run history (basic implementation in progress)

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
- The NL parser is currently rule-based but designed to be replaceable with a free LLM provider (Groq or NVIDIA NIM) by updating the `workflows/services/nl_parser.py` file.
- The execution engine is simulated but structured to be replaced with actual execution logic that interacts with external services.
- The credential vault uses encryption and provides secure storage for sensitive data.
- The frontend currently calls the backend API for parsing and displays the result. Next steps for the frontend include adding workflow list and detail views.

## Next Immediate Steps
1. To enhance the NL parser:
   - Sign up for a free API key from Groq (https://groq.com) or NVIDIA NIM.
   - Add the API key to your `.env` file in the backend branch.
   - Update the `workflows/services/nl_parser.py` file to use the actual LLM API instead of rule-based parsing.
2. To enhance the execution engine:
   - Replace the simulated steps in `workflows/services/execution_engine.py` with actual implementations that:
     * Fetch data from external sources (databases, APIs, file systems)
     * Process the data (transform, filter, aggregate)
     * Deliver the output (send emails, save files, update databases, call webhooks)
   - Consider using asynchronous task queues (like Celery) for long-running workflows.
3. To enhance the frontend:
   - Add components for displaying a list of workflows.
   - Add a workflow detail view that shows the parsed JSON, execution history, and allows manual execution.
   - Implement a workflow visualizer using a library like React Flow or vis.js (if migrating to React) or a JavaScript visualization library.

## References
- [Main README](./README.md)
- [Backend README](./BACKEND_README.md) (in backend branch)
- [Frontend README](./README.md) (in frontend branch)
- Architecture: [docs/architecture.svg](./docs/architecture.svg)
- Flow: [docs/flow.svg](./docs/flow.svg)
