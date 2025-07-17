import streamlit as st
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BACKEND_URL = "https://dyhkp3qhac5xo6q2vanctxrpdm0ejxnw.lambda-url.us-east-1.on.aws/?message=HelloWorld"

st.set_page_config(page_title="Search Places", layout="centered")

st.title("Search Places with Reviews")
st.markdown("Enter your search prompt below (e.g., 'Cafes with live music and Indian cuisine in Hyderabad').")

user_prompt = st.text_input("Search Prompt", "")

if st.button("Search") and user_prompt.strip():
    html_str = ""
    with st.status("Searching...", expanded=True) as status:
        # response = requests.get(BACKEND_URL + "/run", params={"user_prompt": user_prompt})
        response = requests.post(BACKEND_URL, json={"user_prompt": user_prompt, "output_type": "html"}, headers={"Content-Type": "application/json"})
        data = response.text
        if data.startswith("<!DOCTYPE html>"):
            status.update(label="Done! See results below.", state="complete", expanded=False)
            html_str = data
        else:
            status.update(label="Error occurred while processing the request.", state="error", expanded=False)
            logger.error(f"{data}")
            st.error(f"{data}")

    st.markdown("---")

    if html_str:
        st.html(html_str)