#!python3

import irsdk
ir = irsdk.IRSDK()
ir.startup()

filename = 'record-%s-%s-%s.wav' % (ir['SessionUniqueID'], ir['SessionNum'], ir['SessionTime'])
print('Recording: ' + filename)

import queue
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

sd.default.device = 'Microphone (NVIDIA Broadcast), MME'
samplerate = 44100  # Sample rate
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

try:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=1) as file:
        with sd.InputStream(samplerate=samplerate, callback=callback, channels=1):
            print('Press Ctrl+C to stop the recording')
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('Finished')
    exit(0)
