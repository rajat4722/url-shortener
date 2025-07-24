# ui.py
import streamlit as st
import requests

st.title("URL Shortener")

url = st.text_input("Enter the URL to shorten:")

if st.button("Shorten"):
    if not url:
        st.error("Please enter a URL.")
    else:
        resp = requests.post("http://localhost:5000/api/shorten", json={"url": url})
        if resp.status_code == 201:
            data = resp.json()
            st.success(f"Short URL: {data['short_url']}")
            st.write(f"Short code: {data['short_code']}")
        else:
            st.error(resp.json().get("error", "Unknown error"))