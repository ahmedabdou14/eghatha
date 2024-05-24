from db.session import get_db
from db.models import Enrollment


def get_channels(user_id: int) -> list[Enrollment]:
    db = get_db()
    return (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id)
        .order_by(Enrollment.is_approved.desc(), Enrollment.created_at.desc())
        .all()
    )
