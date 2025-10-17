import streamlit as st
from auth import signup, login
from video_processor import process_video
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(page_title="Reelify", page_icon="🎬", layout="centered")

st.title("🎬 Reelify — Video to Reels App")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Select Action", menu)

if "user" not in st.session_state:
    st.session_state.user = None

if choice == "Sign Up":
    st.subheader("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        st.session_state.user = signup(email, password)

elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.user = login(email, password)

if st.session_state.user:
    st.success("You're logged in ✅")
    process_video()
