from pydub import AudioSegment
import os
import pyaudio
import random
# Imposta la cartella contenente i file WAV
folder = 'wav/'

def play(sound):
    # Apertura di un flusso audio
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sound.sample_width),
                    channels=sound.channels,
                    rate=sound.frame_rate,
                    output=True)
    # Riproduzione del suono
    stream.write(sound.raw_data)
    # Chiusura del flusso audio
    stream.stop_stream()
    stream.close()
    p.terminate()

while True:
# Scansione della cartella alla ricerca di file WAV
	numero= len([f for f in os.listdir(folder)if os.path.isfile(os.path.join(folder,f))])
	rand= random.randint(1, int(numero))
	randnamefile = str(rand)+".wav"
	sound = AudioSegment.from_wav(os.path.join(folder, randnamefile))
	print ("Playng;"+randnamefile)
	play(sound)

'''for filename in os.listdir(folder):
if filename.endswith('.wav'):
	# Apertura del file audio WAV
	sound = AudioSegment.from_wav(os.path.join(folder, filename))
	# Riproduzione del file audio WAV
	play(sound)'''
