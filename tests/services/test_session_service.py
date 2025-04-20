import pytest

from sqlmodel import create_engine, SQLModel, Session, select

from brobot.services.session import SessionService
from brobot.models import TrainingSession, Scenario, SessionMessage, ScenarioChapter
from brobot.dto import TrainingSessionWithScenarioAndMessagesDTO
from brobot.dto import SessionMessageDTO


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


@pytest.mark.asyncio
async def test_get_complete_session_returns_model(session):
    # Prepare a scenario and a training session
    scenario = Scenario(title="Test Scenario", description="Desc")
    session.add(scenario)
    session.commit()
    session.refresh(scenario)

    training_session = TrainingSession(user_id=1, scenario_id=scenario.id)
    session.add(training_session)
    session.commit()

    service = SessionService(session)
    result = await service.get_complete_session(training_session.id)

    assert result is not None
    assert isinstance(result, TrainingSession)
    assert result.id == training_session.id


@pytest.mark.asyncio
async def test_get_complete_session_returns_none(session):
    service = SessionService(session)
    result = await service.get_complete_session(9999)
    assert result is None


@pytest.mark.asyncio
async def test_generate_answer_persists_and_returns_message(session, monkeypatch):
    # Prepare scenario and chapter
    scenario = Scenario(title="Test Scenario", description="Desc")
    session.add(scenario)
    session.commit()
    session.refresh(scenario)

    chapter = ScenarioChapter(title="Chapter 1", order=1, scenario_id=scenario.id)
    session.add(chapter)
    session.commit()

    # Create a training session
    training_session = TrainingSession(user_id=1, scenario_id=scenario.id)
    session.add(training_session)
    session.commit()
    session.refresh(training_session)

    # Stub the generate_answer function in the service module
    async def fake_generate_answer(scenario, current_chapter, messages, context):
        return "Fake answer"

    monkeypatch.setattr("brobot.services.session.generate_answer", fake_generate_answer)

    service = SessionService(session)
    result = await service.generate_answer(training_session.id)

    assert isinstance(result, SessionMessageDTO)
    assert result.content == "Fake answer"

    # Verify the message was persisted in the database
    db_messages = session.exec(
        select(SessionMessage).where(SessionMessage.session_id == training_session.id)
    ).all()
    assert any(m.content == "Fake answer" for m in db_messages)
