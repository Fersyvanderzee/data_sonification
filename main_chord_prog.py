from functions import *
from midiutil.MidiFile import MIDIFile

chords = get_progression('I–V–vi–IV', 'C', 'Major')

result_chords = []

for chord in chords:
    notes = get_chord_notes(chord)
    pitches = []
    for note in notes:
        pitch = get_chord_note_pitch(note)
        pitches.append(pitch)
    result_chords.append(pitches)

mf = MIDIFile(1)

time = 0
track = 0
duration = 4
track_name = 'test_chords'

mf.addTrackName(track, time, track_name)
mf.addTempo(track, time, 110)


for chord in result_chords:
    for pitch in chord:
        mf.addNote(0, 0, pitch, time, duration, 85)
    time += duration

with open(f'{track_name}.mid', 'wb') as output_file:
    mf.writeFile(output_file)
print(f'Done! Midi file: {track_name}.mid')






