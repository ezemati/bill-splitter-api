from sqlalchemy import create_engine

from ..core import settings

engine = create_engine(
    settings.db.get_sqlalchemy_url(),
    echo=True,
    connect_args={
        # "check_same_thread": True,
        # "check_same_thread": False,
    },
)
