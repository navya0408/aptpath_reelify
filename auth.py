import streamlit as st
import pyrebase

firebase_config = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "databaseURL": st.secrets["firebase"]["databaseURL"],
    "projectId": st.secrets["firebase"]["projectId"],
    "storageBucket": st.secrets["firebase"]["storageBucket"],
    "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
    "appId": st.secrets["firebase"]["appId"]
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.success("✅ Account created successfully! You can now log in.")
        return user
    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str:
            st.warning("⚠️ Email already exists. Please log in instead.")
        elif "INVALID_EMAIL" in error_str:
            st.error("❌ Invalid email format.")
        elif "WEAK_PASSWORD" in error_str:
            st.error("❌ Weak password (min 6 characters).")
        else:
            st.error(f"❌ Signup failed: {e}")
        return None

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success(f"✅ Logged in as {email}")
        return user
    except Exception as e:
        error_str = str(e)
        if "INVALID_LOGIN_CREDENTIALS" in error_str or "INVALID_PASSWORD" in error_str:
            st.error("❌ Invalid email or password.")
        elif "EMAIL_NOT_FOUND" in error_str:
            st.warning("⚠️ Email not found. Please sign up first.")
        else:
            st.error(f"❌ Login failed: {e}")
        return None
