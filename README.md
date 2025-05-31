# 🎧 English Accent Analyzer

A streamlit-based web application that analyzes English accents from video URLs. This tool downloads videos, extracts audio, applies noise reduction, and classifies English accents using machine learning.

## 🚀 Live Demo

http://167.172.57.242:8501/

## ✨ Features

- **Video URL Support**: Accepts YouTube URLs and direct video links (MP4, etc.)
- **Audio Extraction**: Automatically extracts audio from downloaded videos
- **Noise Reduction**: Optional audio denoising for better accent detection
- **Accent Classification**: Identifies English accent types (British, American, Australian, etc.)
- **Confidence Scoring**: Provides confidence percentage for accent predictions
- **AI-Powered Summaries**: Generates human-readable explanations of results

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Audio Processing**: MoviePy, LibROSA, Deep Filternet
- **Video Download**: yt-dlp
- **Machine Learning**: Hugging Face Transformers (Wav2Vec2)
- **AI Summaries**: OpenRouter API (Mistral)

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API key (for AI summaries)

## ⚡ Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/zakariae200/Accent-detection.git
cd accent-analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

To get an OpenRouter API key:
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Generate an API key from your dashboard

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Paste Video URL**: Enter a YouTube URL or direct video link
2. **Configure Options**: 
   - Toggle noise canceling on/off (recommended: ON)
3. **Click "Analyze"**: The tool will:
   - Download the video
   - Extract audio
   - Apply noise reduction (if enabled)
   - Analyze the accent
   - Generate a summary

## 🎯 Output Format

The tool provides:
- **Accent Classification**: E.g., "American", "British", "Australian"
- **Confidence Score**: Percentage indicating model confidence
- **Audio Previews**: Original and denoised audio playback
- **AI Summary**: Plain English explanation of the results

## 🧪 Testing

### Test with Sample URLs

**YouTube Video Example:**
```
https://www.youtube.com/watch?v=SAMPLE_VIDEO_ID
```

**Direct MP4 Example:**
```
https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4
```

### Expected Workflow
1. Video downloads to `downloads/` directory
2. Audio extracts to `audio/` directory
3. Denoised audio saves to `audio/reduced/` directory
4. Temporary files are cleaned up after analysis

## 📁 Project Structure

```
accent-analyzer/
├── app.py                      # Main Streamlit application
├── accent_analyzer.py          # Core accent analysis logic
├── accent_summary.py           # AI summary generation
├── test_video_url_download.py  # Video download functionality
├── test_audio_extraction.py    # Audio extraction from video
├── noise_reduce.py             # Audio denoising
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🔧 Configuration

### Supported Video Sources
- YouTube videos
- Direct MP4/AVI/MOV links
- Loom recordings
- Most video hosting platforms

### Audio Processing
- **Sample Rate**: 16kHz (automatically converted)
- **Format**: Supports MP3, WAV, MP4 audio
- **Noise Reduction**: Uses Deep Filternet for enhancement

### Model Information
- **Base Model**: `dima806/english_accents_classification`
- **Architecture**: Wav2Vec2 for sequence classification
- **Supported Accents**: Multiple English variants

## 🚨 Troubleshooting

### Common Issues

**1. Video Download Failed**
- Check if URL is accessible and public
- Some platforms may block downloads
- Try with a different video URL

**2. Audio Extraction Error**
- Ensure video contains audio track
- Check if video file downloaded completely

**3. Model Loading Issues**
- First run may take time to download the model
- Ensure stable internet connection
- Model files are cached after first download

**4. OpenRouter API Error**
- Verify your API key in `.env` file
- Check API key permissions and credits

### Performance Notes
- First analysis may take longer (model download)
- Longer videos require more processing time
- Noise reduction adds ~30 seconds to processing

## 🔒 Privacy & Security

- Videos are downloaded temporarily and deleted after processing
- Audio files are cleaned up automatically
- No data is stored permanently on the server
- API calls to OpenRouter are for summary generation only

## 📝 Development Notes

### Key Components

**accent_analyzer.py**: Core ML pipeline
- Lazy loading of Hugging Face model
- Audio preprocessing with LibROSA
- Accent classification and confidence scoring

**noise_reduce.py**: Audio enhancement
- Deep Filternet integration
- Automatic noise reduction
- Quality improvement for better analysis

**app.py**: Streamlit interface
- User-friendly web interface
- Real-time processing feedback
- Audio preview capabilities

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify environment variables are set properly
