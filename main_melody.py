from functions import *
import random
from midiutil.MidiFile import MIDIFile

allowed_notes = get_scale('C', 'Major')

i = 0
max_length = 128

vals = []

while i < max_length:
    random_val = random.randint(45, 92)
    pitch = find_note(random_val, allowed_notes)
    duration = random.randint(1, 2)
    vals.append([pitch, duration])
    i += duration

mf = MIDIFile(1)

time = 0
track = 0
track_name = 'test_melody'

mf.addTrackName(track, time, track_name)
mf.addTempo(track, time, 110)

for val in vals:
    pitch = val[0]
    duration = val[1]

    mf.addNote(0, 0, pitch, time, duration, 85)
    time += duration

with open(f'{track_name}.mid', 'wb') as output_file:
    mf.writeFile(output_file)
print(f'Done! Midi file: {track_name}.mid')




