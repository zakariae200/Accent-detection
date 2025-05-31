import torch
import torchaudio
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
import librosa
import numpy as np
import os

# Model loading function to allow lazy loading
def load_model():
    """
    Load the accent classification model and feature extractor.
    
    Returns:
        tuple: (model, feature_extractor)
    """
    model_name = "dima806/english_accents_classification"
    model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    return model, feature_extractor

# Global variables for lazy loading
_model = None
_feature_extractor = None

def get_model_and_extractor():
    """
    Get the model and feature extractor, loading them if necessary.
    
    Returns:
        tuple: (model, feature_extractor)
    """
    global _model, _feature_extractor
    if _model is None or _feature_extractor is None:
        _model, _feature_extractor = load_model()
    return _model, _feature_extractor

# Load and preprocess the audio
def load_audio(file_path):
    """
    Load and preprocess audio file for accent analysis.
    
    Parameters:
        file_path (str): Path to the audio file
        
    Returns:
        tuple: (audio_data, sample_rate)
    """
    # Load audio with librosa
    audio, sr = librosa.load(file_path, sr=16000)
    return audio, sr

# Predict accent
def predict_accent(file_path):
    """
    Predict the accent in an audio file.
    
    Parameters:
        file_path (str): Path to the audio file
        
    Returns:
        tuple: (accent_label, confidence_score)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
        
    # Get or load model
    model, feature_extractor = get_model_and_extractor()
    
    # Load and process audio
    audio, sr = load_audio(file_path)
    inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt", padding=True)
    
    # Make prediction
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Get results
    predicted_class_id = torch.argmax(logits).item()
    predicted_label = model.config.id2label[predicted_class_id]
    confidence = torch.softmax(logits, dim=1)[0][predicted_class_id].item()
    
    # Get all accent probabilities
    all_probs = torch.softmax(logits, dim=1)[0].tolist()
    all_accents = {model.config.id2label[i]: float(prob) for i, prob in enumerate(all_probs)}
    
    return predicted_label, confidence

# Get detailed accent analysis
def get_detailed_accent_analysis(file_path):
    """
    Get detailed accent analysis including all possible accents and their probabilities.
    
    Parameters:
        file_path (str): Path to the audio file
        
    Returns:
        dict: Detailed accent analysis results
    """
    # Get or load model
    model, feature_extractor = get_model_and_extractor()
    
    # Load and process audio
    audio, sr = load_audio(file_path)
    inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt", padding=True)
    
    # Make prediction
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Get top prediction
    predicted_class_id = torch.argmax(logits).item()
    predicted_label = model.config.id2label[predicted_class_id]
    confidence = torch.softmax(logits, dim=1)[0][predicted_class_id].item()
    
    # Get all accent probabilities
    all_probs = torch.softmax(logits, dim=1)[0].tolist()
    all_accents = {model.config.id2label[i]: float(prob) for i, prob in enumerate(all_probs)}
    
    # Sort accents by probability (highest first)
    sorted_accents = sorted(all_accents.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "top_accent": predicted_label,
        "confidence": confidence,
        "confidence_percent": confidence * 100,
        "all_accents": sorted_accents,
        "file_analyzed": os.path.basename(file_path)
    }



