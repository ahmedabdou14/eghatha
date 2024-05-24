import folium
import streamlit as st
from PIL import Image
import pathlib
from service.incident import get_incidents
from utils import get_mid_location, priority_color
from streamlit_folium import st_folium

try:
    im = Image.open(pathlib.Path("./app/public/eghatha.jpg").absolute())
except Exception:
    im = Image.open(pathlib.Path("./public/eghatha.jpg").absolute())

st.set_page_config(
    page_title="Eghatha",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extreme.com",
        "Report a bug": "https://www.extreme.com",
        "About": "https://www.extreme.com",
    },
)


def main():
    st.markdown("<center> <h1>Eghatha</h1> </center>", unsafe_allow_html=True)

    eventsMap = folium.Map(
        location=get_mid_location(),
        zoom_start=7,
    )

    incidents = get_incidents()
    for incident in incidents:
        folium.Marker(
            location=[incident.lat, incident.lon],
            tooltip=incident.context,
            popup=folium.Popup(
                html=f"""
                    <a href='https://eghatha.streamlit.app?incident={incident.id}' target='_blank'>
                        <img src='{incident.image}' style='width: 200px;'>
                    </a>
                """
            ),
            icon=folium.Icon(color=priority_color(incident.priority), icon="info-sign"),
        ).add_to(eventsMap)

    st_folium(eventsMap, width=1500, height=700)


main()
