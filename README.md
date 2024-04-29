# Media Insights Application

## Overview
The Media Insights application is built to process and analyze audio and video files efficiently. It leverages advanced technologies like Google Cloud's Speech-to-Text for transcriptions, OpenAI's GPT models for summarization, and Spacy for text enhancement. This tool is designed to provide deep insights into media content, making it invaluable for content creators, marketers, and researchers.

## Key Features
- **Audio Splitting:** Breaks down large audio files into smaller chunks for more efficient processing.
- **Transcription:** Converts spoken language into written text using Google Cloud’s Speech-to-Text service.
- **Text Enhancement:** Enhances the readability and structure of transcripts using Spacy.
- **Summary Generation:** Utilizes OpenAI's GPT-3.5 to generate concise summaries of the transcribed text.
- **Embedding Generation:** Generates text embeddings for advanced data analysis and machine learning applications.
- **Database Integration:** Stores all processed data efficiently in a SingleStore database.

## Getting Started

### Prerequisites
- Python 3.8+
- Google Cloud account with Speech-to-Text API access
- OpenAI API key
- SingleStore Database access

### Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/media-insights-application.git
cd media-insights-application
pip install -r requirements.txt

### Configuration
Create a `python` file and update it with your API keys and database configuration:

```python
# config.py
google_cloud_api_key = 'YOUR_GOOGLE_CLOUD_API_KEY'
openai_api_key = 'YOUR_OPENAI_API_KEY'
config = {
   'user': 'DB_USER',
   'password': 'DB_PASSWORD',
   'host': 'DB_HOST',
   'database': 'DB_NAME',
   'port': DB_PORT
}

## Usage
To use this system, follow these steps:

1. **Setup Configuration**: Ensure you have created the `config.py` file with all necessary credentials and configurations as described in the Configuration section.
2. **Install Dependencies**: Run `pip install -r requirements.txt` to install all required Python packages.
3. **Process Files**: Execute the script with the desired audio or video file path:
   ```bash
   python process_media_file.py --file_path 'path_to_your_file.mp4'

 
