from sqlalchemy import create_engine

from ..core import settings

engine = create_engine(
    f"postgresql+psycopg://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}",
    echo=True,
    connect_args={
        # "check_same_thread": True,
        # "check_same_thread": False,
    },
)
