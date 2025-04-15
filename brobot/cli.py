import json
import typer
from sqlmodel import Session
from brobot.database import engine, init_db
from brobot.models import Scenario, ScenarioChapter

app = typer.Typer()


@app.command()
def import_scenario(file: str):
    """
    Import a scenario with its chapters from a JSON file into the database.

    The JSON file must contain the fields required by ScenarioCreate and ChapterCreate,
    for example:
    {
      "title": "My Scenario",
      "description": "A description of my scenario",
      "chapters": [
        {
          "title": "Chapter 1",
          "content": "Content of chapter 1",
          "order": 1,
          "meta": {}
        }
      ]
    }
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        typer.echo(f"Error reading file: {e}")
        raise typer.Exit(code=1)

    try:
        # Extract chapters and validate scenario data
        chapters_data = data.pop("chapters", [])
    except Exception as e:
        typer.echo(f"Error validating scenario data: {e}")
        raise typer.Exit(code=1)

    # Open a session and import the scenario with its chapters
    with Session(engine) as session:
        scenario = Scenario(
            title=data["title"],
            description=data["description"],
        )
        session.add(scenario)
        session.commit()
        session.refresh(scenario)

        for chapter_data in chapters_data:
            try:
                chapter = ScenarioChapter(
                    id=chapter_data.get("id"),
                    content=chapter_data.get("content"),
                    title=chapter_data["title"],
                    order=chapter_data["order"],
                    meta=chapter_data.get("meta", {}),
                    scenario_id=scenario.id,
                )
                session.add(chapter)
            except Exception as e:
                typer.echo(f"Error validating chapter data: {e}")
                raise typer.Exit(code=1)

        session.commit()
        typer.echo(f"Scenario imported successfully with id: {scenario.id}")


if __name__ == "__main__":
    init_db()
    app()
