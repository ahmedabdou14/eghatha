import folium
import streamlit as st
from PIL import Image
import pathlib
import settings
from service.incident import get_incidents
from utils import get_mid_location, priority_color
from streamlit_folium import st_folium
import st_pages

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
        "Get Help": "https://www.linkedin.com/in/ahmedashraf14/",
        "Report a bug": "https://github.com/ahmedabdou14/eghatha/issues",
        "About": "https://github.com/ahmedabdou14/eghatha",
    },
)
st_pages.hide_pages(["incident"])

base_url = (
    "https://eghatha.streamlit.app"
    if settings.ENV == "prod"
    else "http://localhost:8501"
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
                    <a href='{base_url}/incident?id={incident.id}' target='_blank'>
                        <img src='{incident.image}' style='width: 200px;'>
                    </a>
                """
            ),
            icon=folium.Icon(color=priority_color(incident.priority), icon="info-sign"),
        ).add_to(eventsMap)

    folium.Marker(
        location=get_mid_location(),
        tooltip="You are here",
        icon=folium.Icon(color="black", icon="location-arrow", prefix="fa"),
    ).add_to(eventsMap)

    st_folium(eventsMap, width=1500, height=700, return_on_hover=False, returned_objects=[], key="map")


main()
