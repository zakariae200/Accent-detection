import os
from df.enhance import enhance, init_df, load_audio, save_audio

def denoise_audio(input_path, output_path=None):
    """
    Apply noise reduction to an audio file.
    
    Parameters:
    - input_path (str): Path to the input audio file
    - output_path (str, optional): Path where the denoised audio will be saved. If None,
      it will be saved in the 'audio/reduced' directory with the original filename + '_cleaned.wav'
      
    Returns:
    - str: Path to the denoised audio file
    """
    # Create output path if not specified
    if output_path is None:
        output_dir = "audio/reduced"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract the base name of the input audio file (without extension)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # Define the output audio file path using the original filename
        output_path = os.path.join(output_dir, f"{base_name}_cleaned.wav")
    else:
        # Ensure directory exists for the specified output path
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Initialize the model
    model, df_state, _ = init_df()

    # Load your audio file (must be 48kHz mono WAV)
    audio, _ = load_audio(input_path, sr=df_state.sr())

    # Apply noise reduction
    enhanced = enhance(model, df_state, audio)

    # Save the enhanced audio
    save_audio(output_path, enhanced, df_state.sr())
    
    return output_path



