from midiutil.MidiFile import MIDIFile


class Midifile:
    time = 0
    track = 0

    def __init__(self, pitches, bpm, track_name, max_length, duration):
        mf = MIDIFile(1)

        mf.addTrackName(self.track, self.time, track_name)
        mf.addTempo(self.track, self.time, bpm)

        for pitch in pitches:
            if self.time < max_length:
                mf.addNote(self.track, 0, pitch, self.time, duration, 100)
                self.time += duration
            else:
                break

        with open(f'{track_name}.mid', 'wb') as output_file:
            mf.writeFile(output_file)
        print(f'Done! Midi file: {track_name}.mid')
