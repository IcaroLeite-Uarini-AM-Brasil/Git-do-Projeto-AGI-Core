# AGI Core Architecture Notes

## Security
- Use environment variables for Neo4j credentials and runtime configuration.
- Protect execution toolchains with explicit permission checks.
- Use deterministic guardrails before taking high-impact actions.

## Production hardening
- Add CI pipelines, linting, and unit tests.
- Add Docker and health checks for distributed workers.
- Prefer secret managers over `.env` files in deployment.
