# Brobot

[![CI](https://github.com/amrltqt/brobot/actions/workflows/ci.yml/badge.svg)](https://github.com/amrltqt/brobot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Description

Brobot is an open-source platform that enhances human learning through interactive, bot-assisted courses.
Students progress through teacher-crafted lessons with personalized support from a bot that strictly follows the course content.

## Installation

Before you start, ensure you have the following prerequisites installed:
* [Python 3.12+](https://www.python.org/downloads/)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Make](https://www.gnu.org/software/make/)


You have to initialize a `.env.sh` file in the root of the project. You can use the provided `.env.sh.example` file as a template. 

```shell
cp .env.sh.example .env.sh
```

Then, open the `.env.sh` file and set the environment variables according to your configuration.
You can set the following environment variables in the `.env.sh` file:

* `DATABASE_URL`: The URL of the database to use. (exemple: `postgresql://brobot:password@postgres:5432/brobot`)
* `OPENAI_API_KEY`: The OpenAI API key to use for the bot. (exemple: `sk-...`)
* `BROBOT_DATABASE_USER`: The user to use for the database. (exemple: `brobot`)
* `BROBOT_DATABASE_PASSWORD`: The password to use for the database. (exemple: `password`)
* `BROBOT_DATABASE_NAME`: The name of the database to use. (exemple: `brobot`)

```shell
export OPENAI_API_KEY=<your_openai_api_key>
export DATABASE_URL=postgresql://brobot:password@postgres:5432/brobot

export BROBOT_DATABASE_USER=brobot
export BROBOT_DATABASE_PASSWORD=password
export BROBOT_DATABASE_NAME=brobot
```

Then simplest way to start is to use the provided `docker compose` file.

```shell
git clone git@github.com:amrltqt/brobot.git
cd brobot
make reset # This will build the docker images and start the containers
```
This will initialize a database and start a server plus a web client available on `http://localhost:3000`.

## Development

The current docker compose file is built for development. It mounts the current directory into the container, so you can edit the code and see the changes immediately.
The server is running on port 8000 and the web client is running on port 3000.
The database is running on port 5432 and is accessible from the host machine.
