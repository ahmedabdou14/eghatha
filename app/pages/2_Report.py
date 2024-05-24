import st_pages
import streamlit as st
from enum import StrEnum
from openai import OpenAI
from streamlit_tags import st_tags
from service.incident import report
from streamlit_mic_recorder import speech_to_text
from utils import img_to_base64

import settings

st_pages.hide_pages(["incident"])


class StateKey(StrEnum):
    TAGS_GENERATED = "tags_generated"
    IMAGE_NAME = "image_name"
    CONTEXT = "context"


client = OpenAI(api_key=settings.OPENAPI_KEY)


def generate_description(image_base64):
    """Generates a description of the image using the GPT-o model."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I am a local reporting this image during a disaster, generate a maximum of 10 distinct tags tags to explain urgent situation to crisis responders, give tags as bullet points only. If image is not a disaster, please do not reply with any text.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64,
                        },
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content


def extract_tags(description: str) -> list[str]:
    """Extracts tags from the description."""
    return [tag.strip() for tag in description.split("\n") if tag]


def main():
    st.title("Incident Reporting Form")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        tags = []

        if (
            st.session_state.get(StateKey.TAGS_GENERATED, None) is None
            and st.session_state.get(StateKey.IMAGE_NAME, None) != uploaded_file.name
        ):
            with st.spinner("Generating description..."):
                image_base64 = img_to_base64(uploaded_file)
                description = generate_description(image_base64)

                if not description:
                    st.error("Failed to generate description.")
                else:
                    tags = extract_tags(description)
                    st.session_state[StateKey.TAGS_GENERATED] = tags

        tags = st_tags(
            label="Tags",
            text="Type and press enter",
            value=tags,
            suggestions=["Urgent", "Help", "Assistance", "Emergency", "Disaster"],
            maxtags=10,
            key=StateKey.TAGS_GENERATED,
        )

        st.session_state[StateKey.IMAGE_NAME] = uploaded_file.name

        st.text_input(
            "Context",
            placeholder="Use the button below to convert voice-to-text",
            value=st.session_state.get(StateKey.CONTEXT, ""),
            key=StateKey.CONTEXT,
        )
        stt = speech_to_text(language="en", just_once=True, key="STT")
        if stt:
            st.session_state[StateKey.CONTEXT] = stt
            st.rerun()

        if st.button("Submit"):
            if not st.session_state.get(StateKey.TAGS_GENERATED, None):
                st.error("Please generate tags before submitting.")
            if not st.session_state.get(StateKey.CONTEXT, None):
                st.error("Please provide context before submitting.")
            else:
                try:
                    report(
                        img=img_to_base64(uploaded_file),
                        tags=st.session_state[StateKey.TAGS_GENERATED],
                        context=st.session_state[StateKey.CONTEXT],
                    )
                except Exception as e:
                    print(e)
                    st.error("Failed to report the incident.")
                else:
                    st.success("Thank you for reporting the incident. Our team is on it!")


main()
