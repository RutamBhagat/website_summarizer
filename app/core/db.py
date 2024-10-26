from sqlmodel import Session, create_engine, SQLModel, select
from app.crud import user as crud
from app.core.config import settings
from app.models import User, UserCreate

# Create engine with SQLite connect_args for better concurrent access
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), connect_args={"check_same_thread": False}
)

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Create all tables first
    SQLModel.metadata.create_all(engine)

    # Then try to create the superuser if it doesn't exist
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
