import st_pages
import streamlit as st

from service.channels import get_channels

from settings import USER_ID


st_pages.hide_pages(["incident"])


def main():
    st.title("My Channels")

    enrollments = get_channels(USER_ID)
    if not enrollments:
        st.write("You are not enrolled in any channel.")
        return

    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown("## Incident ID")
    with col2:
        st.markdown("## Date")
    with col3:
        st.markdown("## Description")
    with col4:
        st.markdown("## Status")

    st.markdown("---", unsafe_allow_html=True)
    enrolled_channels = [e for e in enrollments if e.is_approved]

    for enrollment in enrolled_channels:
        with st.container():
            col1, col2, col3, col4 = st.columns(4, gap="large")
            incident = enrollment.incident
            with col1:
                st.write(f"INC{incident.id}")
            with col2:
                st.write(incident.created_at.strftime("%Y-%m-%d %H:%M"))
            with col3:
                st.write(incident.context)
            with col4:
                if enrollment.is_approved:
                    st.link_button("Open", f"/incident?id={incident.id}")
                else:
                    st.write("Pending Approval")

    st.markdown("---", unsafe_allow_html=True)
    pending_channels = [e for e in enrollments if not e.is_approved]

    for enrollment in pending_channels:
        with st.container():
            col1, col2, col3, col4 = st.columns(4, gap="large")
            incident = enrollment.incident
            with col1:
                st.write(f"INC{incident.id}")
            with col2:
                st.write(incident.created_at.strftime("%Y-%m-%d %H:%M"))
            with col3:
                st.write(incident.context)
            with col4:
                st.write("Pending Approval")


main()
