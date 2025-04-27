from typing import Optional, List

import requests

from pydantic import HttpUrl
from sqlmodel import Session, select
from brobot.models import Scenario, ScenarioChapter

from brobot.dto import CreateScenarioDTO
from brobot.dto.scenario_chapter import ScenarioChapterWithoutContentDTO
from brobot.dto.scenario_with_chapter import ScenarioWithChapterDTO


class ScenarioService:
    """
    Service class for managing scenarios regarding their creation, retrieval, and deletion.
    """

    def __init__(self, session: Session):
        self.session = session

    def get(self, scenario_id: int) -> Optional[ScenarioWithChapterDTO]:
        """
        Retrieve a scenario by its ID.
        Args:
            scenario_id (int): The ID of the scenario to retrieve.
        Returns:
            Optional[ScenarioWithChapterDTO]: The scenario with its chapters, or None if not found.
        """
        scenario = self.session.exec(
            select(Scenario).where(Scenario.id == scenario_id)
        ).first()

        if not scenario:
            return None

        return ScenarioWithChapterDTO(
            id=scenario.id,
            title=scenario.title,
            description=scenario.description,
            created_at=scenario.created_at,
            chapters=[
                ScenarioChapterWithoutContentDTO(
                    id=chapter.id,
                    title=chapter.title,
                    order=chapter.order,
                )
                for chapter in scenario.chapters
            ],
        )

    def get_all(self) -> List[ScenarioWithChapterDTO]:
        """
        Retrieve all scenarios with their chapters.

        Returns:
            List[ScenarioWithChapterDTO]: A list of scenarios with their chapters.
        """

        scenarios = self.session.exec(select(Scenario)).all()
        return [
            ScenarioWithChapterDTO(
                id=s.id,
                title=s.title,
                description=s.description,
                created_at=s.created_at,
                chapters=[
                    ScenarioChapterWithoutContentDTO(
                        id=c.id,
                        title=c.title,
                        order=c.order,
                    )
                    for c in s.chapters
                ],
            )
            for s in scenarios
        ]

    def delete(self, scenario_id: int) -> bool:
        """
        Delete a scenario and its chapters.

        Args:
            scenario_id (int): The ID of the scenario to delete.

        Returns:
            bool: True if the scenario was deleted, False otherwise.
        """
        scenario = self.session.get(Scenario, scenario_id)
        if not scenario:
            return False

        chapters = self.session.exec(
            select(ScenarioChapter).where(ScenarioChapter.scenario_id == scenario_id)
        ).all()
        for chapter in chapters:
            self.session.delete(chapter)

        self.session.delete(scenario)
        self.session.commit()
        return True

    def create(self, scenario: CreateScenarioDTO) -> Scenario:
        """
        Create a new scenario with its chapters.

        Args:
            scenario (CreateScenarioDTO): The scenario data to create.
        Returns:
            Scenario: The created scenario object.
        """
        scenario_model = Scenario(
            title=scenario.title,
            description=scenario.description,
        )
        self.session.add(scenario_model)
        self.session.commit()
        self.session.refresh(scenario_model)

        for chapter in scenario.chapters:
            chapter_model = ScenarioChapter(
                title=chapter.title,
                order=chapter.order,
                content=chapter.content,
                scenario_id=scenario_model.id,
            )
            self.session.add(chapter_model)

        self.session.commit()
        return scenario_model

    def import_github(
        self, url: HttpUrl, slug: str
    ) -> Optional[ScenarioWithChapterDTO]:
        """
        Import a scenario from a GitHub URL.

        Args:
            url (str): The GitHub URL to import the scenario from.

        Returns:
            Optional[ScenarioWithChapterDTO]: The imported scenario with its chapters, or None if not found.
        """

        # Check if the URL is valid
        # https://github.com/amrltqt/brobot/blob/master/data/scenarios/introduction-sql.json

        # Extract the file path from the URL to get the raw content
        # https://raw.githubusercontent.com/amrltqt/brobot/master/data/scenarios/introduction-sql.json

        if not url.host == "github.com":
            raise ValueError("Invalid GitHub URL")

        if not url.path.endswith(".json"):
            raise ValueError("Invalid file type. Only .json files are supported.")

        # Extract the file path from the URL
        # https://github.com/amrltqt/brobot/blob/master/data/scenarios/introduction-sql.json
        # Example: https://raw.githubusercontent.com/amrltqt/brobot/refs/heads/master/data/scenarios/introduction-sql.json
        raw_url = "https://raw.githubusercontent.com" + url.path.replace(
            "blob/", ""
        ).replace("refs/heads/", "")
        print(raw_url)
        # Fetch the content from the raw URL

        response = requests.get(raw_url)
        if response.status_code != 200:
            raise ValueError("Failed to fetch the file from GitHub")
        content = response.json()
        if not content:
            raise ValueError("Empty content")

        # Create the scenario and chapters
        scenario = Scenario(
            slug=slug,
            title=content["title"],
            description=content["description"],
        )
        self.session.add(scenario)
        self.session.commit()
        self.session.refresh(scenario)

        for chapter in content["chapters"]:
            chapter_model = ScenarioChapter(
                title=chapter["title"],
                order=chapter["order"],
                content=chapter["content"],
                scenario_id=scenario.id,
            )
            self.session.add(chapter_model)
        self.session.commit()

        return ScenarioWithChapterDTO(
            id=scenario.id,
            title=scenario.title,
            description=scenario.description,
            created_at=scenario.created_at,
            chapters=[
                ScenarioChapterWithoutContentDTO(
                    id=chapter_model.id,
                    title=chapter_model.title,
                    order=chapter_model.order,
                )
                for chapter_model in scenario.chapters
            ],
        )
