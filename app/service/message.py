from db.session import get_db
from db.models import Message


def get_incident_messages(incident_id: int) -> list[Message]:
    db = get_db()
    return db.query(Message).filter_by(incident_id=incident_id).all()


def create_message(
    *,
    incident_id: int,
    message: str,
    created_by: int,
) -> Message:
    db = get_db()
    msg = Message(
        incident_id=incident_id,
        text=message,
        created_by=created_by,
    )
    db.add(msg)
    db.commit()
    return msg
