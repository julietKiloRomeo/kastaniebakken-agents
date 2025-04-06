FROM python:3.12


ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1

RUN apt update && apt install -y nodejs npm
RUN curl -fsSL https://bun.sh/install | bash

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt


ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug" ]
