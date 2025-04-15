from sqlmodel import create_engine, Session, SQLModel
from brobot.core.config import settings

# Create the SQLModel engine using the DATABASE_URL from settings.
engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    """
    Dependency that provides a SQLModel session.
    Yields a new session for each request and ensures it is closed after use.
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Initialize the database by importing all models and creating the tables.
    This function should be called at application startup.
    """

    SQLModel.metadata.create_all(engine)
