from moviepy import VideoFileClip
import os

def extract_audio(video_path, output_audio_path=None):
    """
    Extract audio from a video file.
    
    Parameters:
    - video_path (str): Path to the video file
    - output_audio_path (str, optional): Path where the audio will be saved. If None,
      it will be saved in the 'audio' directory with the same name as the video file.
      
    Returns:
    - str: Path to the extracted audio file
    """
    # Create audio directory if not specified in output path
    if output_audio_path is None:
        audio_dir = "audio"
        os.makedirs(audio_dir, exist_ok=True)
        
        # Extract the base name of the video file (without extension)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # Define the output audio file path within the audio directory
        output_audio_path = os.path.join(audio_dir, f"{base_name}.mp3")
    else:
        # Ensure directory exists for the specified output path
        os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
    
    # Load the video file
    video = VideoFileClip(video_path)

    # Extract audio
    audio = video.audio

    # Save the audio file
    audio.write_audiofile(output_audio_path)

    # Close the video and audio clips
    audio.close()
    video.close()
    
    return output_audio_path


