FROM python:3.12.6

RUN mkdir /ujin_xac

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

WORKDIR /ujin_xac

ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:0.6.4 /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --group dev --frozen --no-install-project

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

ENV PATH="/ujin_xac/.venv/bin:$PATH"
