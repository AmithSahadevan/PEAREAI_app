import streamlit as st
import subprocess
import sys
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import sys
from pathlib import Path

# Add the parent directory to Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from queue_manager import email_queue
from config import EMAIL_CONFIG

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

def send_email(recipient_email, video_path):
    """Send email with video attachment"""
    sender_email = EMAIL_CONFIG["sender_email"]
    sender_password = EMAIL_CONFIG["sender_password"]
    
    if sender_password == "your-app-specific-password-here":
        print("Error: Please set up your email password in config.py")
        return False
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your PEARE AI Generated Video"
    
    body = "Thank you for using PEARE AI! Your video has been generated and is attached to this email."
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the video file
    with open(video_path, 'rb') as f:
        video_attachment = MIMEApplication(f.read(), _subtype="mp4")
        video_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(video_path))
        msg.attach(video_attachment)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_video_cli(prompt):
    try:
        print("\n=== Starting Video Generation ===")
        print(f"Prompt: {prompt}")
        
        # Keep the local virtual environment path
        venv_path = "C:/Users/amith/OneDrive/Desktop/miniproject/project1/env"
        if not Path(venv_path).exists():
            print(f"Error: Virtual environment not found at {venv_path}")
            return False, f"Virtual environment not found at {venv_path}"
            
        # Activate virtual environment
        if sys.platform == "win32":
            activate_script = venv_path + "/Scripts/activate.bat"
        else:
            activate_script = venv_path + "/bin/activate"
            
        if not Path(activate_script).exists():
            print(f"Error: Activation script not found at {activate_script}")
            return False, f"Activation script not found at {activate_script}"
            
        print(f"Activating virtual environment at {venv_path}")
        
        # Install required packages first
        print("\nInstalling required packages...")
        required_packages = [
            "torch",
            "torchvision",
            "gradio",
            "numpy",
            "pillow",
            "safetensors",
            "easydict",
            "diffusers",
            "ftfy",
            "transformers"
        ]
        
        for package in required_packages:
            print(f"Installing {package}...")
            try:
                subprocess.run([f"{venv_path}/Scripts/pip", "install", package], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to install {package}: {e}")
        
        # Keep the local script path
        script_path = "C:/Users/amith/OneDrive/Desktop/miniproject/project1/generate_video_with_audio.py"
        if not Path(script_path).exists():
            print(f"Error: Could not find generate_video_with_audio.py at {script_path}")
            return False, f"Could not find generate_video_with_audio.py at {script_path}"

        # Change to the directory containing generate_video_with_audio.py
        working_dir = Path(script_path).parent
        print(f"Working directory: {working_dir}")
        
        # Add the project directory to PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = str(working_dir) + os.pathsep + env.get("PYTHONPATH", "")
        
        # Clean the prompt of any special characters that might cause issues
        clean_prompt = prompt.replace('"', '').replace("'", "")
        
        # Construct the command to run generate_video_with_audio.py with only the specified parameters
        cmd = [
            f"{venv_path}/Scripts/python",
            script_path,
            "--prompt", clean_prompt,
            "--resolution", "832x480",
            "--num-frames", "81",
            "--num-steps", "30",
            "--guidance-scale", "7.5",
            "--flow-shift", "5.0",
            "--seed", "-1",
            "--negative-prompt", "",
            "--tea-cache", "0.0",
            "--tea-cache-step", "20",
            "--riflex", "auto",
            "--profile", "4",
            "--lora-dir", "./loras",
            "--vae-config", "2",
            "--transformer", "ckpts/wan2.1_text2video_1.3B_bf16.safetensors",
            "--t2v"
        ]
        
        print("\nExecuting command:")
        print(" ".join(cmd))
        
        # Run the command and wait for completion
        print("\nStarting video generation process...")
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=working_dir,
            text=True,
            env=env
        )
        
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        
        # Print the output for debugging
        print("\nProcess output:")
        print(stdout)
        if stderr:
            print("\nProcess errors:")
            print(stderr)
        
        if process.returncode != 0:
            print(f"Error: Process failed")
            print(f"Error details: {stderr}")
            return False, f"Process failed: {stderr}"
        
        print("Video generation completed successfully!")
        print("===============================")
        return True, "Video generation completed successfully"
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, f"Error starting video generation: {str(e)}"

# Create header with logo
st.markdown("""
<div class="header">
    <div class="logo">
        <span>🍐</span> PEARE AI
    </div>
</div>
""", unsafe_allow_html=True)

# Main content
st.markdown('<div class="title">What video should I create?</div>', unsafe_allow_html=True)

# Create the prompt input container
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Text input for the prompt - now using the full width
prompt = st.text_area(
    label="Video Description",
    height=100, 
    placeholder="Enter a detailed description of the video you want to generate...",
    label_visibility="collapsed"
)

# Generate button - now placed under the text field
generate = st.button("Generate", key="generate_button")

st.markdown('</div>', unsafe_allow_html=True)

# Update the generate button handler
if generate and prompt:
    if not prompt.strip():
        st.error("Please enter a video description before generating.")
    else:
        # Get the next email from the queue
        recipient_email = email_queue.get_next_email()
        if recipient_email:
            # Show immediate success message
            st.success("""
            🎉 Your video will be sent to your email soon!
            
            Thank you for using PEARE AI!
            
            Note: Video generation typically takes 30-50 minutes depending on length and settings.
            """)
            
            # Start video generation and wait for completion
            with st.spinner('Generating video... This may take 30-50 minutes...'):
                success, message = generate_video_cli(prompt)
                if success:
                    # Keep the local output directory path
                    output_dir = Path("C:/Users/amith/OneDrive/Desktop/miniproject/project1/output/gradio")
                    print(f"Looking for video in: {output_dir}")
                    
                    if output_dir.exists():
                        video_files = list(output_dir.glob("*.mp4"))
                        print(f"Found {len(video_files)} video files")
                        
                        if video_files:
                            latest_video = max(video_files, key=lambda x: x.stat().st_mtime)
                            print(f"Latest video: {latest_video}")
                            
                            # Send email with video
                            print(f"Attempting to send email to: {recipient_email}")
                            if send_email(recipient_email, str(latest_video)):
                                st.success(f"Video generated and sent to {recipient_email}!")
                                print("Email sent successfully")
                            else:
                                st.error("Failed to send email. Please contact support.")
                                print("Failed to send email")
                        else:
                            st.error("No video files found in output directory")
                            print("No video files found")
                    else:
                        st.error("Video output directory not found")
                        print(f"Output directory not found: {output_dir}")
                else:
                    st.error(f"Sorry, there was an error: {message}")
                    print(f"Video generation failed: {message}")
        else:
            st.error("No email found in queue. Please try again later.")
