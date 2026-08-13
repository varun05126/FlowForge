# FlowForge — turn plain-English requests into automated workflows.

FlowForge is a platform that allows users to automate tasks by describing them in natural language. The system parses the request, extracts the necessary components (trigger, source, conditions, action), and generates a structured workflow that can be executed automatically.

## Problem it solves
Many users want to automate repetitive tasks but lack the technical skills to set up complex integrations and scheduling. FlowForge bridges this gap by converting plain English into actionable workflows.

## Architecture
![System Architecture](docs/architecture.svg)

## Request-to-Execution Flow
![Workflow Execution Flow](docs/flow.svg)

## Branch structure
- `main` — Contains shared documentation, architecture diagrams, and configuration files.
- `frontend` — React (Vite) application for building and viewing workflows.
- `backend` — Node.js (Express) API for handling workflow CRUD, NL parsing, and execution.

## Local setup instructions

### Backend
1. Checkout the backend branch: `git checkout backend`
2. Install dependencies: `npm install`
3. Copy `.env.example` to `.env` and fill in the required values (never commit real `.env`).
4. Start the development server: `npm run dev`

### Frontend
1. Checkout the frontend branch: `git checkout frontend`
2. Install dependencies: `npm install`
3. Copy `.env.example` to `.env` and set `VITE_API_BASE_URL` (e.g., `http://localhost:5000`).
4. Start the development server: `npm run dev`

## Tech stack
- **Frontend**: React, Vite
- **Backend**: Node.js, Express
- **Database**: SQLite (for development), PostgreSQL (for production)
- **NL Parser**: Integrated with free LLM providers like Groq or NVIDIA NIM (stubbed in initial scaffold)
- **Others**: Docker (optional), JWT for authentication

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
