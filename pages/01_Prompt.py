import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="PEARE AI",
    page_icon="🍐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply minimalist styling
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1d391kg, .css-12oz5g7 {display: none;}
    .stDeployButton {display:none;}
    
    /* Custom font and base styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean container styling */
    .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
        background-color: #0F0F0F;
    }
    
    /* Header styling */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Logo styling */
    .logo {
        font-size: 22px;
        font-weight: 500;
        color: white;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.5px;
    }
    
    /* Profile button styling */
    .profile-btn {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 99px;
        padding: 8px 16px;
        border: none;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .profile-btn:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Input container styling */
    .input-container {
        max-width: 800px;
        margin: 0 auto 2rem auto;
    }
    
    /* Title styling */
    .title {
        font-size: 28px;
        font-weight: 500;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        letter-spacing: -0.5px;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
        box-shadow: none !important;
        transition: border-color 0.2s;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(255, 255, 255, 0.3);
        box-shadow: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #5E5AFA;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        width: 100%;
        height: 46px;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #4D48E0;
    }
    
    /* Generate button specific styling */
    .generate-button {
        margin-top: 12px;
        max-width: 800px;
    }
    
    /* Action buttons styling */
    .action-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }
    
    .action-button {
        background-color: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.7);
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .action-button:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Output container styling */
    .output-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 2rem;
    }
    
    /* Info styling */
    .stAlert {
        background-color: rgba(94, 90, 250, 0.1);
        color: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(94, 90, 250, 0.3);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Create header with logo and profile button
st.markdown("""
<div class="header">
    <div class="logo">
        <span>🍐</span> PEARE AI
    </div>
    <button class="profile-btn">Log in</button>
</div>
""", unsafe_allow_html=True)

# Main content
st.markdown('<div class="title">What video should I create?</div>', unsafe_allow_html=True)

# Create the prompt input container
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Text input for the prompt - now using the full width
prompt = st.text_area("", 
                      height=100, 
                      placeholder="Enter a detailed description of the video you want to generate...",
                      label_visibility="collapsed")

# Generate button - now placed under the text field
generate = st.button("Generate", key="generate_button")

st.markdown('</div>', unsafe_allow_html=True)

# Bottom action buttons
st.markdown("""
<div class="action-buttons">
    <button class="action-button">Recent</button>
    <button class="action-button">Examples</button>
    <button class="action-button">Templates</button>
</div>
""", unsafe_allow_html=True)

# Demo output (only show if generate button is clicked)
if generate and prompt:
    st.info("Video generation in progress... This may take a few moments.")
    
    # Placeholder for video output
    st.markdown("""
    <div class="output-container">
        <p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 20px;">Video preview will appear here</p>
        <div style="font-size: 48px;">🎬</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download option
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="Download Video",
            data=b"placeholder",  # This would be your actual video data
            file_name="claude_ai_video.mp4",
            mime="video/mp4",
            disabled=True  # Enable this when you have actual video data
        )
