import st_pages
import streamlit as st

from db.session import get_db
from db.models import Incident
from annotated_text import annotated_text

st_pages.hide_pages(["incident"])

id = int(st.query_params.get("id", 1))


@st.cache_data
def get_incident(incident_id: int) -> Incident | None:
    db = get_db()
    return db.query(Incident).get(incident_id)


def main(id: int):
    incident = get_incident(id)
    if not incident:
        st.error("Incident not found")
        return

    st.markdown(
        f"<center> <h1>Incident {incident.id}</h1> </center>", unsafe_allow_html=True
    )

    st.text(f"Created at: {incident.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    st.image(incident.image, caption="Incident Image", use_column_width=True, width=500)

    annotated_text(
        [
            (tag, "") if i % 2 == 0 else "  "
            for i, tag in enumerate(incident.tags)
            if len(tag) > 1
        ]
    )

    if st.button("Back"):
        st.switch_page("Home.py")


main(id)
