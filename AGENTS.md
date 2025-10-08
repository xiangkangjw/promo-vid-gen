# Repository Guidelines

## Project Structure & Module Organization
The workspace splits into `backend` (FastAPI AgentOS services) and `frontend` (Next.js UI). Backend source lives in `backend/src`: `agent_os_server.py` mounts the API, `agents/` groups agent implementations, and `workflows/` encapsulates orchestration logic. Persistent config lives in Docker assets at `backend/Dockerfile` and `docker-compose.yml`. Backend tests belong in `backend/tests`, mirroring package names. The frontend keeps route handlers in `frontend/app`, reusable visuals in `frontend/components`, shared hooks in `frontend/hooks`, and utilities in `frontend/lib`; shared types sit in `frontend/types`.

## Build, Test, and Development Commands
- `cd backend && uvicorn src.agent_os_server:app --reload`: local API with hot reload.
- `cd backend && docker-compose up --build`: full stack with Postgres and Redis.
- `cd backend && pytest`: run Python test suite.
- `cd frontend && npm run dev`: Next.js dev server at http://localhost:3000.
- `cd frontend && npm run lint` / `npm run type-check` / `npm run build`: linting, TypeScript validation, and production build.

## Coding Style & Naming Conventions
Backend Python follows Black defaults (88 cols, 4-space indent). Keep modules snake_case, classes PascalCase, and functions lower_snake_case. Run `black src tests` and `flake8 src tests` before pushing. Favor type hints on public functions and docstrings at workflow entry points. Frontend TypeScript leans on ESLint’s `next` config; prefer function components, PascalCase file names for components, and co-locate styles via Tailwind utility classes.

## Testing Guidelines
Target meaningful pytest coverage for each agent and workflow; name files `test_<unit>.py` and use fixtures for API clients. When adding async flows, annotate tests with `pytest.mark.asyncio`. The frontend currently lacks automated tests—gate UI changes with `npm run lint` and `npm run type-check`, and add component specs under `frontend/__tests__` using Vitest or Testing Library when introduced. Document any manual test steps in the PR.

## Commit & Pull Request Guidelines
Follow imperative, present-tense messages and prefer Conventional Commit prefixes (`feat:`, `fix:`, `chore:`). Keep atomic commits scoped to one concern. Pull requests should summarize intent, link tracking issues, note environment or schema changes, and include screenshots or clips for UI updates and video output changes. Request review once CI passes and all checklist items are satisfied.

## Environment & Secrets
Copy `.env.example` into both `backend/.env` and `frontend/.env.local` as needed, populating API keys such as `OPENAI_API_KEY`, `GOOGLE_PLACES_API_KEY`, and `PEXELS_API_KEY`. Docker services expect these variables at runtime. Never commit secrets; use your platform’s secret store for deployments.
