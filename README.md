# Brobot

[![CI](https://github.com/amrltqt/brobot/actions/workflows/ci.yml/badge.svg)](https://github.com/amrltqt/brobot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Description

Brobot is an open-source platform that enhances human learning through interactive, bot-assisted courses.
Students progress through teacher-crafted lessons with personalized support from a bot that strictly follows the course content.

## Installation

Before you start, ensure you have the following prerequisites installed:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Make](https://www.gnu.org/software/make/)


```shell
git clone git@github.com:amrltqt/brobot.git
cd brobot
```

You have to initialize a `.env.sh` file in the root of the project. You can use the provided `.env.sh.example` file as a template. 

```shell
cp .env.sh.example .env.sh
```
Inject the `OPENAI_API_KEY` in the .env.sh file to use the OpenAI API. You can get an API key from [OpenAI](https://platform.openai.com/signup).

```shell
export OPENAI_API_KEY=sk-...
```

Then simplest way to start is to use the provided `make reset` command to initialize the docker containers.

This will initialize a database and start a server plus a web client available on `http://localhost:3000`.

## Development

The current docker compose file is built for development. It mounts the current directory into the container, so you can edit the code and see the changes immediately.
The server is running on port 8000 and the web client is running on port 3000.
The database is running on port 5432 and is accessible from the host machine.

Check the [Environment](docs/env.md) for the available environment variables.