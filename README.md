

# Media Insights Application
## PART - 1
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


## PART - 2

## `C#` Project User Interface

 The `C#` part of our project encompasses a user-friendly interface designed to interact with the media insights application. Here's what you need to know about using the C# application:

## Overview

The user interface is built using ASP.NET Core MVC, providing a responsive web application that allows users to search and view summarized insights from audio and video files processed by the backend.

### Key Features

- **Query Interface**: Users can input questions to search within the transcriptions for specific insights or information.
- **Summary Display**: The interface displays concise summaries and key points extracted from media files, enhancing the usability and accessibility of the processed data.
- **Interactive Results**: Results are presented in an interactive format, allowing users to delve deeper into specific areas of the media transcription.
- **Media Management**: Users can upload, manage, and view media files directly through the web interface.

### Running the Application

To run the C# project locally:

1. **Open the Solution**: Navigate to the folder containing the C# project and open the solution file in Visual Studio.
2. **Restore Packages**: Ensure all NuGet packages are restored to resolve dependencies.
3. **Set Configuration**: Update the `appsettings.json` or equivalent configuration file with necessary API keys and database connections as detailed in the Configuration section.
4. **Run the Application**: Use the 'Run' button in Visual Studio or use the command line within the project directory:
   ```bash
   dotnet run

### Access the Application: Open your web browser and navigate to http://localhost:{port}, where {port} is the port number specified in your project settings.
- **Dependencies: Ensure that your system has the following installed:
- ***.NET Core 3.1 SDK or later
- ***ASP.NET runtime
 
