#!/usr/bin/python
from google.cloud import speech
from pydub import AudioSegment
import argparse, wave, array, math, glob, os, pyaudio, shutil, io
import numpy as np
import requests
import os

#----------------------------------------------
#list_of_files = glob.glob('test/*.wav')
#latest_file = max(list_of_files, key=os.path.getctime)
#scritta = latest_file[5:-4]
#----------------------------------------------

parser = argparse.ArgumentParser(description='AudioMic->WAVE')
parser.add_argument('-t', action='store', dest='secondi', type=int, help='Inserisci i Secondi di registrazione', default=3)
results = parser.parse_args()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./lib/freespeech-374309-5a6c7dd7c7da.json"

# Record in chunks of 1024 samples
chunk = 1024

# 16 bits per sample
sample_format = pyaudio.paInt16
chanels = 2

# Record at 44400 samples per second
smpl_rt = 44400
seconds = results.secondi
#conta file
folder = 'wav/'
numero= len([f for f in os.listdir(folder)if os.path.isfile(os.path.join(folder, f))])
filename = "./wav/"+str(int(numero)+1)+".wav"

# Create an interface to PortAudio
pa = pyaudio.PyAudio()

stream = pa.open(format=sample_format, channels=chanels,
                 rate=smpl_rt, input=True,
                 frames_per_buffer=chunk)

#os.system('clear')
print('Inizio Registrazione...')
print('Secondi:')
print(seconds)
# Initialize array that be used for storing frames
frames = []

# Store data in chunks for X seconds
for i in range(0, int(smpl_rt / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate - PortAudio interface
pa.terminate()

if results is None:
	os.execl(sys.executable, sys.executable, *sys.argv)

print('FATTO !!! ')

# Save the recorded data in a .wav format
sf = wave.open(filename, 'wb')
sf.setnchannels(chanels)
sf.setsampwidth(pa.get_sample_size(sample_format))
sf.setframerate(smpl_rt)
sf.writeframes(b''.join(frames))
sf.close()


# Creates google client
client = speech.SpeechClient()

# Full path of the audio file, Replace with your file name
file_name = os.path.join(os.path.dirname(__file__),filename)

#Loads the audio file into memory
with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=2,
    language_code="it-IT",
)

# Sends the request to google to transcribe the audio
response = client.recognize(request={"config": config, "audio": audio})
# print("OK inviato!!")
# Reads the response
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
    testone=format(result.alternatives[0].transcript)
    r = requests.get('https://api.telegram.org/bot6022035627:AAHcIt3tXDXXlhWDrGoieUJs1NE8o3Ar7vo/sendMessage?chat_id=-849404497&text='+testone,
                      headers={'Accept': 'application/json'})
    #sound = AudioSegment.from_wav('test.wav')
    #sound.export('test.mp3', format='mp3')
    # shutil.copy('test/test.wav', 'test/'+format(result.alternatives[0].transcript)+'.wav')
    #os.rename('test.wav', format(result.alternatives[0].transcript)+'.wav')
    #os.rename('test.mp3', format(result.alternatives[0].transcript)+'.mp3')
    

file_object = open('testo.txt', 'a')
file_object.write(format(result.alternatives[0].transcript +", "))
file_object.close()

