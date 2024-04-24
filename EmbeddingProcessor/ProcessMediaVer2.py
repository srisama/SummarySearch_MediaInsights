
import io
import openai

from google.cloud import speech
from pydub import AudioSegment
from google.cloud import speech
import os
import mysql.connector
import spacy 

 

# Configure  API keys and Weaviate / Single Store instance URL here
google_cloud_api_key = 'AIzaSyAjPTteaYWNvin2cjAR7dzXzuoiKxIzcpI'  
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

def transcribe_and_format_audio(file_path):
    client = speech.SpeechClient()
    audio_chunks = split_audio(file_path)
    raw_transcript = ""

    for chunk in audio_chunks:
        if chunk.channels > 1:
            chunk = chunk.set_channels(1)
        
        byte_io = io.BytesIO()
        chunk.export(byte_io, format="wav")
        byte_io.seek(0)
        content = byte_io.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
            sample_rate_hertz=chunk.frame_rate,
            enable_automatic_punctuation=True # Enable automatic punctuation
        )

        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            raw_transcript += result.alternatives[0].transcript + " "

    # Enhance the transcript formatting
    enhanced_transcript = enhance_transcript_formatting(raw_transcript)
    return raw_transcript, enhanced_transcript

def enhance_transcript_formatting(raw_transcript):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(raw_transcript)
    sentences = []
    for sent in doc.sents:
        # Capitalize the first letter of each sentence
        cleaned_sentence = sent.text.strip().capitalize()
        # Replace incorrect breaks and common misrecognitions
        cleaned_sentence = cleaned_sentence.replace("Queen", "Queen,")  # Example correction
        sentences.append(cleaned_sentence)
    enhanced_transcript = " ".join(sentences)
    return enhanced_transcript


def summarize_text(text, model="gpt-3.5-turbo-instruct", max_tokens=150, chunk_size=4096):
    # Split the text into manageable chunks within the model's token limits
   chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
   summaries = []

   for chunk in chunks:
       prompt = f"Create a well-punctuated, concise summary for the following content, organizing it into bullet points or a structured paragraph that clearly distinguishes key concepts and their relationships: {chunk}"
       response = openai.Completion.create(
           model=model,
           prompt=prompt,
           max_tokens=max_tokens
       )
       chunk_summary = response.choices[0].text.strip()
       summaries.append(chunk_summary)
    # Combine summaries of each chunk into a single structured summary
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



def store_in_singlestore(filename, filetype, category, raw_transcript, summary, embedding, enhanced_transcript):
    connection = get_database_connection()
    cursor = connection.cursor()

    # Adjust SQL to include both raw and enhanced transcripts
    embeddings_str = ', '.join(str(e) for e in embedding)
    sql = f"""
    INSERT INTO MediaFile (filename, filetype, category, transcript, summary, contentVector, enhancedTranscript)
    VALUES (%s, %s, %s, %s, %s, JSON_ARRAY_PACK('[{embeddings_str}]'), %s)
    """
    values = (filename, filetype, category, raw_transcript, summary, enhanced_transcript)

    cursor.execute(sql, values)
    connection.commit()

    print(f"Inserted record ID: {cursor.lastrowid}")
    cursor.close()
    connection.close()


def process_media_file(filepath):
    """
    Process an audio/video file through the pipeline.
    """
    # Unpack both raw and enhanced transcripts returned from the function
    raw_transcript, enhanced_transcript = transcribe_and_format_audio(filepath)
    
    # Use the enhanced transcript for summarization and embeddings
    summary = summarize_text(raw_transcript)
    embedding = generate_embeddings(raw_transcript)  # Generate embeddings from the enhanced transcript

    # Store using the raw transcript but display the enhanced one
    store_in_singlestore("Meeting_02Feb2024.mp4", "video", "GoogleSolar",raw_transcript, summary, embedding, enhanced_transcript)

if __name__ == "__main__":
    process_media_file("Meeting_02Feb2024.mp4")
