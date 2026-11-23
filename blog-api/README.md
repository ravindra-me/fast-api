cd blog-api

# 1. Start Postgres (docker-compose.yml maps it to localhost:5434)

docker compose up -d

# 2. Install dependencies into .venv

uv sync

# 3. Create the tables

uv run alembic upgrade head

# 4. Start the API with auto-reload

uv run fastapi dev app/main.py
