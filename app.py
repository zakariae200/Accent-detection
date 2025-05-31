import streamlit as st
import os
import shutil
import time
from test_video_url_download import download_video
from test_audio_extraction import extract_audio
from noise_reduce import denoise_audio
from accent_analyzer import predict_accent

# Constants
download_dir = "downloads"
audio_dir = "audio"
reduced_dir = os.path.join(audio_dir, "reduced")

# Ensure output folders exist
os.makedirs(download_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(reduced_dir, exist_ok=True)

st.set_page_config(page_title="Accent Analyzer", page_icon="🎤", layout="centered")
st.title("🎧 English Accent Analyzer")
st.markdown("""
Paste a **YouTube video URL** or a direct video link below. This tool will:
1. Download the video
2. Extract the speaker's audio
3. Optionally apply noise reduction
4. Analyze and classify the English accent
""")

# Sidebar options
with st.sidebar:
    st.header("🛠 Audio Processing")
    enable_denoise = st.checkbox("🎛 Enable Noise Canceling", value=True)
    st.markdown("---")
    st.info("This feature enhances clarity if the audio has background noise.")

# Main form
video_url = st.text_input("🔗 Paste Video URL")

if st.button("🚀 Analyze") and video_url:
    # Generate a unique ID for this session
    unique_id = str(int(time.time()))

    # Define expected paths
    video_output_path = os.path.join(download_dir, f"video_{unique_id}.mp4")
    audio_output_path = os.path.join(audio_dir, f"audio_{unique_id}.mp3")
    cleaned_output_path = os.path.join(reduced_dir, f"audio_{unique_id}_cleaned.wav")

    with st.spinner("📥 Downloading video..."):
        download_video(video_url, output_path=download_dir, filename=f"video_{unique_id}")

    if not os.path.exists(video_output_path):
        st.error("❌ Failed to download video.")
        st.stop()

    st.video(video_output_path)

    with st.spinner("🎙 Extracting audio from video..."):
        extract_audio(video_output_path, output_audio_path=audio_output_path)

    # Remove video after extracting audio
    os.remove(video_output_path)

    final_audio_path = audio_output_path

    # Optional: noise reduction
    if enable_denoise:
        st.info("🎚 Noise canceling is enabled. Cleaning audio...")
        final_audio_path = denoise_audio(audio_output_path, output_path=cleaned_output_path)

    # Display audio players
    st.markdown("---")
    st.subheader("🔊 Audio Previews")
    st.markdown("**🎧 Original Audio:**")
    st.audio(audio_output_path, format="audio/mp3")
    if enable_denoise:
        st.markdown("**🔇 Denoised Audio:**")
        st.audio(cleaned_output_path, format="audio/wav")

    # Analyze accent
    with st.spinner("🧠 Analyzing accent..."):
        label, confidence = predict_accent(final_audio_path)
        from accent_summary import generate_summary

        # Get LLM-based explanation
        summary = generate_summary(label, confidence)

    # Display results
    st.markdown("---")
    st.subheader("🎯 Accent Analysis Result")
    st.markdown(f"""
    <div style='padding:1rem;border-radius:10px;background:#f9f9f9;border:1px solid #ccc;'>
        <h3 style='color:#333;'>🗣 Accent: <span style='color:#0066cc'>{label}</span></h3>
        <h4 style='color:#555;'>Confidence Score: <b>{confidence:.2%}</b></h4>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 📝 Accent Summary")
    st.success(summary)

    # Cleanup audio files
    try:
        if os.path.exists(audio_output_path):
            os.remove(audio_output_path)
        if enable_denoise and os.path.exists(cleaned_output_path):
            os.remove(cleaned_output_path)
    except Exception as e:
        st.warning(f"⚠️ Could not delete some temporary files: {e}")

    st.markdown("""
    <style>
    .stSpinner > div > div {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
