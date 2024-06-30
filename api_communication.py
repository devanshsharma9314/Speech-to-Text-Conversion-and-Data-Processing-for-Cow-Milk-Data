import requests
#Use API key of your AssemblyAi account
from api_secrets import API_KEY_ASSEMBLYAI 
import time


#upload
# Define API endpoints
upload_endpoint ="https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# Set the authorization headers with the API key
headers = {'authorization': API_KEY_ASSEMBLYAI}


# Function to upload an audio file to AssemblyAI
def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    # Post request to upload the audio file
    response = requests.post(upload_endpoint,headers=headers,data=read_file(filename))

    
    # Get the upload URL from the response
    audio_url = response.json()['upload_url']
    return audio_url


#transcribe

# Function to initiate transcription of the uploaded audio file
def transcribe(audio_url):
    json = { "audio_url": audio_url}
    # Post request to start transcription
    response = requests.post(transcript_endpoint, json=json, headers=headers )

    # Get the job ID from the response
    job_id = response.json()['id']
    return job_id





#poll

# Function to poll the transcription job status
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    #print(polling_response.json())
    return polling_response.json()

# Function to get the result URL of the transcription
def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        
        # Wait for 30 seconds before polling again
        print('Waiting 30 seconds...')
        time.sleep(30)


# save transcript

# Function to save the transcription result to a file
def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)
    if data:
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data['text'])
        print('Transcription saved!!')
        return text_filename
    elif error:
        print("Error!!", error)
        return "end"
