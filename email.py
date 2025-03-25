import streamlit as st
import time
import os

# Configure the Streamlit page
st.set_page_config(
    page_title="PEARE AI - Email Subscription",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🍐"
)

# Add custom CSS for dark theme and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
    
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .logo {
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 46px;
        letter-spacing: 3px;
        color: #ffffff;
        margin-bottom: 30px;
    }
    .form-label {
        font-size: 18px;
        color: #BBBBBB;
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        width: 100%;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #3d8b40;
    }
    .centered {
        text-align: center;
    }
    footer {
        text-align: center;
        margin-top: 50px;
        color: #666;
        font-size: 14px;
    }
    /* Hide sidebar navigation */
    .css-1d391kg, [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Display the logo as plain text in Montserrat font
st.markdown('<div class="logo">PEARE AI</div>', unsafe_allow_html=True)

# Create a header for the form
st.markdown('<p class="form-label centered">Enter your email to continue</p>', unsafe_allow_html=True)

# Create the form with email input and continue button
with st.form(key='email_form'):
    # Fixed: Added a proper label and used label_visibility to hide it
    email = st.text_input(
        label="Email Address", 
        placeholder='Your email address',
        label_visibility="collapsed"
    )
    
    # Handle form submission
    submit_button = st.form_submit_button(label='CONTINUE')
    
    if submit_button:
        if email and '@' in email and '.' in email:
            # Store email in session state
            st.session_state.user_email = email
            
            # Redirect to the prompt page using Streamlit's page navigation
            st.switch_page("pages/01_Prompt.py")
        else:
            st.error('Please enter a valid email address')

# Add a footer
st.markdown("""
<footer>
    © 2025 PEARE AI. All rights reserved.
</footer>
""", unsafe_allow_html=True)