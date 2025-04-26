# Brobot


## Description

Brobot is an open-source web platform designed to enhance human learning through interactive, bot-assisted courses.
It allows students to follow step-by-step lessons created by teachers, with personalized guidance from a bot that strictly follow the content of each course.


## Installation


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
docker compose build && docker compose up
```

This will initialize a database and start a server plus a web client available on `http://localhost:3000`.


## Development
If you want to run the project locally without Docker, you can do so by following these steps:

1. Clone the repository:

```shell
git clone git@github.com:amrltqt/brobot.git
cd brobot
```

### Web server 

To install Brobot, install the required dependencies:

* [uv](https://docs.astral.sh/uv/getting-started/installation/)

Once you have `uv` installed, clone the repository and install the required dependencies:

```shell
cd brobot
uv sync --all-extras --dev
```

This will create a virtual environment and install the required dependencies in it for the web server and the bot.

### Web client

The web client is a nextjs application in the app folder.

To install the web client, navigate to the `app` directory and install the required dependencies:

```shell
cd app
npm install
```
This will install the required dependencies for the web client.

## Usage

To run the web server, use the following command:

```shell
source .venv/bin/activate
fastapi run brobot/app.py
```

This will start the web server on `http://localhost:8000`.

In a separate terminal, navigate to the `app` directory and run the following command to start the web client:

```shell
cd app
npm run dev
```

This will start the web client on `http://localhost:3000`.

If you already have some running services on those port, usually fastapi and nextjs will run on `http://localhost:8001` and `http://localhost:3001` respectively.

Once the app is started, you should add a first scenario. 
I started brobot with in mind the idea of training people in SQL, so I created a first example available in the `/data` folder.

Import it in your instance with:

```shell
export PYTHONPATH=$(pwd)

typer brobot.cli run data/scenarios/introduction-sql.json
```