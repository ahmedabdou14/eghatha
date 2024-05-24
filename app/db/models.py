import random
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Incident(Base):
    __tablename__ = "incident"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column()
    context: Mapped[str] = mapped_column()
    _tags: Mapped[str] = mapped_column("tags")
    lat: Mapped[float] = mapped_column()
    lon: Mapped[float] = mapped_column()
    priority: Mapped[int] = mapped_column()

    @property
    def tags(self) -> list[str]:
        return [tag.strip() for tag in self._tags.split(" ") if tag]

    @tags.setter
    def tags(self, value: list[str]):
        self._tags = " ".join(value)
