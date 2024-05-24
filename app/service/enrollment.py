from db.models import Enrollment
from db.session import get_db


def is_enrolled(user_id: int, incident_id: int) -> bool:
    db = get_db()
    return (
        db.query(Enrollment).filter_by(user_id=user_id, incident_id=incident_id).first()
        is not None
    )


def enroll(user_id: int, incident_id: int):
    db = get_db()
    enrollment = Enrollment(user_id=user_id, incident_id=incident_id)
    db.add(enrollment)
    db.commit()
