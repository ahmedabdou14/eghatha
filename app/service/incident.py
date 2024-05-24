import random
from db.models import Incident
from utils import gen_location
from db.session import get_db


def report(
    img: str,
    tags: list[str],
    context: str,
):
    db = get_db()
    lat, lon = gen_location()
    incident = Incident(
        image=img,
        tags=tags,
        context=context,
        lat=lat,
        lon=lon,
        priority=random.randint(1, 5),
    )
    db.add(incident)
    db.commit()


def get_incidents():
    db = get_db()
    return db.query(Incident).all()
