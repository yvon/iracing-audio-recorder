#!python3

import os
from ctypes import windll
import tkinter as tk
from tkinter import filedialog

windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
		initialdir=os.getcwd(),
		title="Select file",
		filetypes=[("Audio Files", "*.wav")]
)

import sounddevice as sd
import soundfile as sf

sd.default.device = 'Speakers (NVIDIA Broadcast), MME'

# Extract data and sampling rate from file
data, fs = sf.read(file_path, dtype='float32')  
sd.play(data, fs)

import sys
import re

search = re.search('record-\d+-(\d+)-(.+)\.wav$', file_path)
session_num = int(search.group(1))
session_time_ms = int(float(search.group(2)) * 1000) # in ms

import irsdk
ir = irsdk.IRSDK()
ir.startup()

ir.replay_search_session_time(session_num, session_time_ms)

status = sd.wait()  # Wait until file is done playing
