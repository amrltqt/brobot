# Environment configuration


Start with an empty `.env.sh` file in the root of the project. You can use the provided `.env.sh.example` file as a template.

```shell
cp .env.sh.example .env.sh
```

## Database

Configure the database connection string and the setup of the database.

You can set the following environment variables in the `.env.sh` file:
* `DATABASE_URL`: The URL of the database to use. (example: `postgresql://brobot:password@postgres:5432/brobot`)
* `BROBOT_DATABASE_USER`: The user to use for the database. (example: `brobot`)
* `BROBOT_DATABASE_PASSWORD`: The password to use for the database. (example: `password`)
* `BROBOT_DATABASE_NAME`: The name of the database to use. (example: `brobot`)

```shell
# For the api service in docker-compose.yml
export DATABASE_URL=postgresql://brobot:password@postgres:5432/brobot

# For the postgres service in docker-compose.yml
export BROBOT_DATABASE_USER=brobot
export BROBOT_DATABASE_PASSWORD=password
export BROBOT_DATABASE_NAME=brobot
```

## Model

Configure the model to use for the bot.
You can set the following environment variables in the `.env.sh` file:

* `OPENAI_BASE_URL`: The base URL of the OpenAI API. (example: `https://api.openai.com/v1`)
* `OPENAI_API_KEY`: The OpenAI API key to use for the bot. (example: `sk-...`)
* `MODEL_NAME`: The model to use for the bot. (example: `gpt-4.1-mini`)

```shell
# For the api service in docker-compose.yml
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_API_KEY=sk-...
export MODEL_NAME=gpt-4.1-mini
```

