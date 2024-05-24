import st_pages
import streamlit as st

from service.user import get_user, default_image_base64
from db.session import get_db
from db.models import Incident
from annotated_text import annotated_text
from settings import USER_ID

from service.message import create_message, get_incident_messages
from service.enrollment import enroll, is_enrolled
from streamlit_chat import message

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

    st.write("\n\n")

    st.text(f"Created at: {incident.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    st.image(incident.image, caption="Incident Image", use_column_width=True, width=500)

    annotated_text(
        [
            (f"{tag}", "") if i % 2 == 0 else " "
            for i, tag in enumerate(incident.tags * 2)
            if len(tag) > 1
        ]
    )

    if not is_enrolled(USER_ID, incident.id):
        if st.button("Enroll", use_container_width=True):
            enroll(USER_ID, incident.id)
            st.success("Enrollment request has been sent to Eghatha admins")
    else:
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<center> <h2>Chat</h2> </center>", unsafe_allow_html=True)
        chat_placeholder = st.empty()

        with chat_placeholder.container(height=500):
            messages = get_incident_messages(id)
            for msg in messages:
                is_me = msg.created_by == USER_ID
                user = get_user(msg.created_by)
                if not user:
                    continue
                logo = user.image or default_image_base64
                message(msg.text, is_user=is_me, logo=logo, key=f"msg:{str(msg.id)}")

        st.session_state["user_input"] = ""

        def on_message():
            user_input = st.session_state["user_input"]
            if user_input:
                create_message(
                    incident_id=id,
                    message=user_input,
                    created_by=USER_ID,
                )
                st.session_state["user_input"] = ""

        with st.spinner("Loading chat"):
            st.text_input("Type a message", key="user_input", value="")
            submit = st.button("Submit", on_click=on_message)
            if submit:
                st.rerun()

    if st.button("Back"):
        st.switch_page("Home.py")


main(id)
