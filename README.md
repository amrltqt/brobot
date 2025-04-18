# Brobot


## Description

Brobot is an open-source web platform designed to enhance human learning through interactive, bot-assisted courses.
It allows students to follow step-by-step lessons created by teachers, with personalized guidance from a bot that strictly follow the content of each course.


## Installation


### Database

Initialize a local SQLite database for development:

```shell
sqlite3 database.db < data/schema.sql
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