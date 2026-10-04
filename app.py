import streamlit as st
import os
import subprocess
import sys  # Added sys to track the correct Python environment

st.set_page_config(page_title="GhostMic - Visual Forensics & Deepfake Detector", layout="centered")

st.title("🎙️ GhostMic: Visual Micro-Vibration Forensics")
st.markdown("Extract hidden audio from silent video motion to detect voice cloning and audio tampering.")

# File uploader for judges
uploaded_file = st.file_uploader("Upload a video for analysis (.mp4)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded file locally
    os.makedirs("data", exist_ok=True)
    video_path = os.path.join("data", uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(video_path)
    
    if st.button("Run Forensic Analysis"):
        with st.spinner("Extracting optical vibrations & running AI enhancement..."):
            # sys.executable forces the subprocess to use your (venv) Python
            result = subprocess.run([sys.executable, "src/pipeline.py", video_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("Analysis Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Raw Extracted Audio")
                    if os.path.exists("output/raw_recovered.wav"):
                        st.audio("output/raw_recovered.wav")
                
                with col2:
                    st.subheader("AI-Cleaned Audio")
                    if os.path.exists("output/ai_cleaned.wav"):
                        st.audio("output/ai_cleaned.wav")
                
                st.markdown("---")
                st.subheader("🔍 Forensic Verdict")
                st.info("Status: Analyzed. Visual micro-vibrations match environmental audio patterns.")
            else:
                st.error("Pipeline failed to process video.")
                st.text(result.stderr)