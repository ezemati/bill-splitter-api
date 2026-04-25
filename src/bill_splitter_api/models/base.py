import uuid

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


# https://github.com/sqlalchemy/sqlalchemy/discussions/10698
# MappedAsDataclass
class ModelBase(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        # note: don't set default here because the value will be set by __init__
        # default=uuid.uuid7,
        # default_factory=uuid.uuid7,
    )

    def __init__(self, **kwargs):
        if "id" not in kwargs:
            # setting id here instead of in the column definition
            # because we want to generate it at object instantiation
            # instead of at flush time
            kwargs["id"] = uuid.uuid7()
        super().__init__(**kwargs)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        table_name = pascal_to_snake(cls.__name__)
        return table_name


def pascal_to_snake(text: str) -> str:
    if not text:
        return ""

    chars = []
    for i, char in enumerate(text):
        if i > 0 and char.isupper():
            prev_char = text[i - 1]

            # Look ahead to see if the next character is lowercase
            # (helps split acronyms from standard words, e.g., 'HTTP' and 'Request')
            next_is_lower = i + 1 < len(text) and text[i + 1].islower()

            # Add an underscore if transitioning from lower/digit to upper,
            # or if transitioning out of an acronym into a normal word
            if prev_char.islower() or prev_char.isdigit() or next_is_lower:
                chars.append("_")

        chars.append(char.lower())

    return "".join(chars)
