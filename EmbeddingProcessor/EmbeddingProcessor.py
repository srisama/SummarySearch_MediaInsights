import io
import openai
import weaviate
from google.cloud import speech
from pydub import AudioSegment
from google.cloud import speech
import os
import mysql.connector




  

# Initialize the OpenAI client
openai.api_key = openai_api_key

# Initialize the Weaviate client
#weaviate_client = weaviate.Client(url=weaviate_instance_url, auth_client_secret=weaviate.auth.AuthApiKey(weaviate_api_key))


# Database connection parameters for SingleStore
config = {
    'user': {Insert vector database username},
    'password': {Insert vector database password},
    'host': {Insert vector database host link},
    'database': {Insert vector database name},
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




def summarize_text(text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Summarize this text: {text}",
        max_tokens=150
    )
    summary = response.choices[0].text.strip()
    return summary

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

# def store_in_weaviate(filename, filetype, category, transcript, summary, embedding):
#     """
#     Store the data in Weaviate.
#     """
#     media_file_data = {
#         "filename": filename,
#         "filetype": filetype,
#         "category": category,
#         "transcript": transcript,
#         "summary": summary,
#         "contentVector": embedding
#     }
#     weaviate_client.data_object.create(media_file_data, "MediaFile")

def store_in_singlestore(filename, filetype, category, transcript, summary, embedding):
    connection = get_database_connection()
    cursor = connection.cursor()

    # # Assuming your SingleStore table has a column for each of these fields
    # sql = "INSERT INTO MediaFile (filename, filetype, category, transcript, summary, contentVector) VALUES (%s, %s, %s, %s, %s, %s)"
    # values = (filename, filetype, category, transcript, summary, str(embedding))  # embedding might need to be processed to fit into the table

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
    store_in_singlestore("Framework_library.mp4", "video", "vectordb", transcript, summary, embedding)

if __name__ == "__main__":
    process_media_file("Framework_library.mp4")
