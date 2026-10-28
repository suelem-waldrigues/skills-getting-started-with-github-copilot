# Copilot instructions for this repository

## Project overview

This repository is a small FastAPI app for Mergington High School: it serves a simple extracurricular activities directory and allows students to sign up for activities. The app is intentionally lightweight and keeps all data in memory, which means the server state resets when the process restarts.

The relevant runtime files are:

- `src/app.py`: FastAPI application, in-memory activity registry, root redirect, and API endpoints
- `src/static/index.html`: browser UI that loads activity data and submits signups
- `src/static/app.js`: frontend logic that calls the API and updates the page
- `src/static/styles.css`: formatting for the page
- `src/README.md`: project-level app docs for this service

## Build, test, and validation commands

There is no repo-specific build pipeline, linter, or package manager configuration beyond the Python requirements.

Use these commands when working locally:

- Install dependencies:
  `pip install -r requirements.txt`
- Run the app from the source directory:
  `cd src && python app.py`
- Or run the app with Uvicorn during development:
  `cd src && uvicorn app:app --reload --port 8000`
- Open the app in a browser:
  `http://localhost:8000/`
- Open the API docs:
  `http://localhost:8000/docs`

Testing setup:

- The repo includes `pytest.ini`, so `pytest` discovery is enabled with `pythonpath = .`.
- Run the full suite with:
  `pytest -q`
- Run a single test by path or keyword, for example:
  `pytest -q tests/test_app.py::test_signup`
  `pytest -q -k signup`

There is no dedicated lint command configured in this repo today. If you add Python checks later, keep them minimal and consistent with the existing project structure.

## High-level architecture

This app is intentionally a single-process, single-file API with a static frontend:

- `src/app.py` defines the FastAPI app and creates the in-memory `activities` dictionary.
- Requests to `/activities` return the current in-memory structure.
- The signup flow is handled by `POST /activities/{activity_name}/signup`, which validates the activity name and appends the email to that activity's `participants` list.
- The root route redirects to `/static/index.html`, so the browser UI and API are served from the same app.
- The frontend in `src/static/` reads from `/activities` and posts signups to the signup endpoint; it does not talk to a database or another service.

This repository is intentionally small and educational. Prefer surgical changes in `src/app.py` and the matching frontend behavior in `src/static/` instead of introducing broader abstractions or service layers.

## Key conventions and repo-specific patterns

- Keep the app state in memory. The `activities` dictionary is the source of truth and resets on server restart.
- Use the activity name as the identifier in the route path, e.g. `Chess Club` or `Programming Class`.
- Preserve the existing shape of each activity entry: `description`, `schedule`, `max_participants`, and `participants`.
- The frontend is served as static assets; when making user-facing changes, update the relevant file under `src/static/` alongside the API behavior.
- The app is intentionally simple and does not include a persistence layer, database models, authentication, or service architecture.
- Follow the current API conventions: `GET /activities` returns JSON, and signups are posted with the email as a query parameter such as `?email=student@mergington.edu`.
- A missing activity should continue to return a 404-style FastAPI `HTTPException` instead of silently creating empty state.

## Practical guidance for future Copilot sessions

- Prefer targeted edits around the API and the static frontend; there is no multi-package app structure to navigate.
- When changing a route or response shape, check both the server and the frontend together because the browser UI depends on the exact JSON fields.
- Do not add persistent storage or a new framework unless the task explicitly requires it.
- Keep changes minimal and consistent with the teaching/demo nature of this project.
