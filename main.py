from functions import *

chords = get_progression(['I', 'V', 'vi', 'IV'], 'C', 'Major')
print(chords)

for chord in chords:
    notes = get_chord_notes(chord)
    pitches = []
    for note in notes:
        pitch = get_chord_note_pitch(note)
        pitches.append(pitch)
    print(pitches)


