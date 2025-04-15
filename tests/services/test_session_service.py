import pytest

from sqlmodel import create_engine, SQLModel, Session, select

from brobot.services.session import SessionService
from brobot.models import TrainingSession, Scenario
from brobot.dto import TrainingSessionWithScenarioAndMessagesDTO


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_get_returns_training_session(session):
    scenario = Scenario(title="Test Scenario", description="Description")
    session.add(scenario)
    session.flush()

    training_session = TrainingSession(user_id=1, scenario_id=scenario.id)
    session.add(training_session)
    session.commit()

    service = SessionService(session)
    result = await service.get(training_session.id)

    assert result is not None
    assert isinstance(result, TrainingSessionWithScenarioAndMessagesDTO)
    assert result.id == training_session.id
    assert result.scenario.title == "Test Scenario"


@pytest.mark.asyncio
async def test_users_sessions_returns_none_if_not_found(session):
    service = SessionService(session)
    result = await service.users_sessions(1)
    assert result is None


@pytest.mark.asyncio
async def test_users_sessions_returns_training_session(session):
    scenario = Scenario(title="Test Scenario", description="Description")
    session.add(scenario)
    session.flush()

    training_session = TrainingSession(user_id=1, scenario_id=scenario.id)
    session.add(training_session)
    session.commit()

    service = SessionService(session)
    result = await service.users_sessions(1)

    assert result is not None
    assert isinstance(result, TrainingSessionWithScenarioAndMessagesDTO)
    assert result.id == training_session.id
    assert result.scenario.title == "Test Scenario"


@pytest.mark.asyncio
async def test_get_or_create_creates_new_training_session(session):
    scenario = Scenario(title="Test Scenario", description="Description")
    session.add(scenario)
    session.commit()

    service = SessionService(session)
    result = await service.get_or_create(user_id=1, scenario_id=scenario.id)

    assert result is not None
    assert isinstance(result, TrainingSessionWithScenarioAndMessagesDTO)
    assert result.scenario.title == "Test Scenario"

    # Verify the session was created in the database
    db_session = session.exec(
        select(TrainingSession).where(TrainingSession.user_id == 1)
    ).first()
    assert db_session is not None
    assert db_session.scenario_id == scenario.id
