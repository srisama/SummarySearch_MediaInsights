import io
import openai

from google.cloud import speech
from pydub import AudioSegment
from google.cloud import speech
import os
import mysql.connector


 

# Configure your API keys and Weaviate instance URL here
google_cloud_api_key = 'AIzaSyAjPTteaYWNvin2cjAR7dzXzuoiKxIzcpI'  # Not needed if you authenticate with service account JSON
openai_api_key = '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'


# Initialize the OpenAI client
openai.api_key = openai_api_key


# Database connection parameters for SingleStore
config = {
   'user': 'admin',
    'password': 'Myvectordb@2024',
    'host': 'svc-e61d79e1-67e9-428b-9467-ec6df011c104-dml.aws-virginia-6.svc.singlestore.com',
    'database': 'EmbeddingsDB',
    'port': 3306
}

def get_database_connection():
    return mysql.connector.connect(**config)



def split_audio(file_path, max_size_in_bytes=10485760):
    audio = AudioSegment.from_file(file_path)
    chunks = []
    
    # Ensure chunk length is at least 1 millisecond to avoid zero or negative values
    total_bytes = len(audio.raw_data)
    chunk_length_in_milliseconds = max(1, int((max_size_in_bytes / total_bytes) * len(audio) * 1000 / audio.frame_rate))
    
    for start in range(0, len(audio), chunk_length_in_milliseconds):
        end = start + chunk_length_in_milliseconds
        if end > len(audio):
            end = len(audio)
        chunk = audio[start:end]
        chunks.append(chunk)
    
    return chunks
def transcribe_audio(file_path):
    client = speech.SpeechClient()

    # Split the audio file if it's too large
    audio_chunks = split_audio(file_path)
    transcript = ""
     
    for chunk in audio_chunks:
        # Convert stereo to mono if necessary
        if chunk.channels > 1:
            chunk = chunk.set_channels(1)
        # Convert the audio chunk to the appropriate format
        byte_io = io.BytesIO()
        chunk.export(byte_io, format="wav")
        byte_io.seek(0)
        content = byte_io.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
            sample_rate_hertz=chunk.frame_rate
        )

        # Perform the transcription
        response = client.recognize(config=config, audio=audio)

        # Concatenate the results
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "

    return transcript.strip()





def summarize_text(text, model="gpt-3.5-turbo-instruct", max_tokens=150, chunk_size=4096):
    # Split the text into chunks that fit within the model's token limit
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []

    for chunk in chunks:
        prompt = f"Summarize this text: {chunk}"
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        chunk_summary = response.choices[0].text.strip()
        summaries.append(chunk_summary)

    # Combine the summaries of each chunk to form the final summary
    full_summary = ' '.join(summaries)
    return full_summary



def generate_embeddings(text):
    """
    Generate embeddings using OpenAI API.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    embedding = response['data'][0]['embedding']
    return embedding



def store_in_singlestore(filename, filetype, category, transcript, summary, embedding):
    connection = get_database_connection()
    cursor = connection.cursor()

   

    # Constructing the embeddings part of the SQL query
    embeddings_str = ', '.join(str(e) for e in embedding)  # Convert embeddings list to a string
    sql = f"""
    INSERT INTO MediaFile (filename, filetype, category, transcript, summary, contentVector)
    VALUES (%s, %s, %s, %s, %s, JSON_ARRAY_PACK('[{embeddings_str}]'))
    """
    values = (filename, filetype, category, transcript, summary)


    cursor.execute(sql, values)
    connection.commit()

    print(f"Inserted record ID: {cursor.lastrowid}")
    cursor.close()
    connection.close()

def process_media_file(filepath):
    """
    Process an audio/video file through the pipeline.
    """
    transcript = transcribe_audio(filepath)
    summary = summarize_text(transcript)
    embedding = generate_embeddings(summary)
    store_in_singlestore("LangChain.mp4", "video", "Lang Chain", transcript, summary, embedding)

if __name__ == "__main__":
    process_media_file("LangChain.mp4")