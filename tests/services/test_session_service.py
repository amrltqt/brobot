import pytest

from sqlmodel import create_engine, SQLModel, Session, select

from brobot.services.session import SessionService
from brobot.models import TrainingSession, Scenario, SessionMessage
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

    assert result is not None
    assert len(result) == 0


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
    assert len(result) == 1
    assert isinstance(result[0], TrainingSessionWithScenarioAndMessagesDTO)
    assert result[0].id == training_session.id


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


@pytest.mark.asyncio
async def test_delete_session_with_messages(session):
    # Create a scenario
    scenario = Scenario(title="Test Scenario", description="Description")
    session.add(scenario)
    session.flush()

    # Create a training session
    training_session = TrainingSession(user_id=1, scenario_id=scenario.id)
    session.add(training_session)
    session.flush()

    # Add messages to the training session
    message1 = SessionMessage(
        content="Message 1", role="user", session_id=training_session.id
    )
    message2 = SessionMessage(
        content="Message 2", role="assistant", session_id=training_session.id
    )
    session.add_all([message1, message2])
    session.commit()

    # Verify messages exist in the database
    messages = session.exec(
        select(SessionMessage).where(SessionMessage.session_id == training_session.id)
    ).all()
    assert len(messages) == 2

    # Delete the training session
    service = SessionService(session)
    result = await service.delete(training_session.id)

    # Verify the session and its messages are deleted
    assert result is True
    deleted_session = session.exec(
        select(TrainingSession).where(TrainingSession.id == training_session.id)
    ).first()
    assert deleted_session is None

    remaining_messages = session.exec(
        select(SessionMessage).where(SessionMessage.session_id == training_session.id)
    ).all()
    assert len(remaining_messages) == 0
