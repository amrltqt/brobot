import pytest
from sqlmodel import create_engine, SQLModel, Session, select

from brobot.services.scenarios import ScenarioService
from brobot.models import Scenario, ScenarioChapter
from brobot.dto import CreateScenarioDTO, CreateScenarioChapterDTO


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_get_returns_none_if_not_found(session):
    service = ScenarioService(session)
    assert service.get(1) is None


def test_get_returns_scenario_with_chapters(session):
    scenario = Scenario(title="Test", description="Desc", slug="test")
    chapter1 = ScenarioChapter(title="C1", content="Content 1", order=1, scenario_id=1)
    chapter2 = ScenarioChapter(title="C2", content="Content 2", order=2, scenario_id=1)

    session.add(scenario)
    session.flush()

    chapter1.scenario_id = scenario.id
    chapter2.scenario_id = scenario.id
    session.add_all([chapter1, chapter2])
    session.commit()

    service = ScenarioService(session)
    result = service.get(scenario.id)

    assert result is not None
    assert result.title == "Test"
    assert len(result.chapters) == 2
    assert result.chapters[0].title == "C1"


def test_get_all_returns_all_scenarios(session):
    s1 = Scenario(title="S1", description="D1", slug="s1")
    s2 = Scenario(title="S2", description="D2", slug="s2")
    session.add_all([s1, s2])
    session.commit()

    service = ScenarioService(session)
    result = service.get_all()

    assert len(result) == 2
    assert result[0].title == "S1"
    assert result[1].title == "S2"


def test_delete_removes_scenario_and_chapters(session):
    scenario = Scenario(title="S", description="D", slug="s")
    session.add(scenario)
    session.flush()

    c = ScenarioChapter(
        title="C", order=1, content="Content 1", scenario_id=scenario.id
    )
    session.add(c)
    session.commit()

    service = ScenarioService(session)
    deleted = service.delete(scenario.id)

    assert deleted is True
    assert session.get(Scenario, scenario.id) is None

    assert (
        session.exec(select(ScenarioChapter).filter_by(scenario_id=scenario.id)).all()
        == []
    )


def test_delete_returns_false_if_not_found(session):
    service = ScenarioService(session)
    assert service.delete(1234) is False


def test_create_scenario(session: Session):
    """
    Test the creation of a Scenario.
    """

    scenario_creation = CreateScenarioDTO(
        slug="test-scenario",
        title="Test Scenario",
        description="This is a test scenario.",
        chapters=[
            CreateScenarioChapterDTO(
                title="Chapter 1", content="Content of chapter 1", order=1, meta={}
            ),
            CreateScenarioChapterDTO(
                title="Chapter 2", content="Content of chapter 2", order=2, meta={}
            ),
        ],
    )

    service = ScenarioService(session)
    scenario = service.create(scenario_creation)

    assert scenario is not None
    assert scenario.title == "Test Scenario"
    assert scenario.description == "This is a test scenario."
    assert len(scenario.chapters) == 2
    assert scenario.chapters[0].title == "Chapter 1"
    assert scenario.chapters[1].title == "Chapter 2"
    assert scenario.chapters[0].order == 1
    assert scenario.chapters[1].order == 2
