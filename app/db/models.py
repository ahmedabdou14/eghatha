import enum
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import sqlalchemy.dialects.postgresql as pg
import datetime as dt
from sqlalchemy.ext.mutable import MutableList


class UserType(enum.StrEnum):
    user = enum.auto()
    admin = enum.auto()


PgUserType = pg.ENUM(UserType, name="user_type")


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
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))

    @property
    def tags(self) -> list[str]:
        return [
            tag.strip().strip("#")
            for tag in self._tags.replace("*", "-").split("-")
            if tag
        ]

    @tags.setter
    def tags(self, value: list[str]):
        self._tags = " ".join(value)


class UserBase(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[UserType] = mapped_column(PgUserType)
    hashed_pwd: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    profession: Mapped[str] = mapped_column(String)
    skills: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(pg.ARRAY(item_type=String)), server_default="{}"
    )
    image: Mapped[str | None] = mapped_column(nullable=True)

    incidents: Mapped[list["Incident"]] = relationship()

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "unknown",
    }


class User(UserBase):
    __tablename__ = None

    __mapper_args__ = {
        "polymorphic_identity": UserType.user,
    }


class Admin(UserBase):
    __tablename__ = None

    __mapper_args__ = {
        "polymorphic_identity": UserType.admin,
    }


class Enrollment(Base):
    __tablename__ = "enrollment"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incident.id"), primary_key=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_approved: Mapped[bool] = mapped_column(default=False)

    incident: Mapped[Incident] = relationship()


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incident.id"))
    text: Mapped[str] = mapped_column()
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
