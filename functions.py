import wave
import array
import random
from PIL import Image


class MusicUtils:
    PITCHES = {
        'A': [33, 45, 57, 69, 81, 93],
        'A#': [34, 46, 58, 70, 82, 94],
        'Bb': [34, 46, 58, 70, 82, 94],
        'B': [35, 47, 59, 71, 83, 95],
        'C': [36, 48, 60, 72, 84, 96],
        'C#': [37, 49, 61, 73, 85, 97],
        'Db': [37, 49, 61, 73, 85, 97],
        'D': [38, 50, 62, 74, 86, 98],
        'D#': [39, 51, 63, 75, 87, 99],
        'Eb': [39, 51, 63, 75, 87, 99],
        'E': [40, 52, 64, 76, 88, 100],
        'F': [41, 53, 65, 77, 89, 101],
        'F#': [42, 54, 66, 78, 90, 102],
        'Gb': [42, 54, 66, 78, 90, 102],
        'G': [43, 55, 67, 79, 91, 103],
        'G#': [44, 56, 68, 80, 92, 104],
        'Ab': [44, 56, 68, 80, 92, 104]
    }


    @classmethod
    def get_random_note(cls, allowed_notes: list, octave: int, length: int):
        """
        Picks a random note from the provided scale (allowed notes).

            Args:
                allowed_notes (list): The allowed notes in a list.
                octave (int): Which octave range should be picked. Between 0 and 5 (both ends included)
                length (int): Length of the melody.

            Returns:
                int: Pitch of the selected random note.
        """

        if not 0 <= octave <= 5:
            raise ValueError('Octave not within range. Pick a number between 0 and 5 (both ends included)')

        result = [random.choice(allowed_notes) for _ in range(length)]
        return [cls.PITCHES[note][octave] for note in result]


    @classmethod
    def find_note(cls, value, allowed_notes: list):
        """
        Finds the nearest allowed note.

            Args:
                value (int, float): The value to be converted.
                allowed_notes (list): The allowed notes in a list.

            Returns:
                int: The closest allowed pitch
        """

        # Initialize variables to track the closest pitch and its difference
        closest_pitch = None
        min_difference = float('inf')

        # Iterate through the allowed notes and find the closest pitch to the given value
        for note in allowed_notes:
            for pitch in cls.PITCHES[note]:
                difference = abs(value - pitch)
                if difference < min_difference:
                    min_difference = difference
                    closest_pitch = pitch

        return closest_pitch


class ScaleUtils:
    @staticmethod
    def get_scale(note: str, mode: str):
        """
        Returns all allowed notes within a scale.

            Args:
                note (str): The root note of the scale.
                mode (str): The mode that provides the allowed notes.

            Returns:
                list: Allowed notes based on the provided note and mode.
        """

        # Define the note order based on the note_dict
        note_order = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        mode_dict = {
            'Major': [0, 2, 2, 1, 2, 2, 2, 1],
            'Natural minor': [0, 2, 1, 2, 2, 1, 2, 2],
            'Harmonic minor': [0, 2, 1, 2, 2, 1, 3, 1],
            'Melodic minor': [0, 2, 1, 2, 2, 2, 2, 1],
            'Dorian': [0, 2, 1, 2, 2, 2, 1, 2],
            'Phrygian': [0, 1, 2, 2, 2, 1, 2, 2],
            'Lydian': [0, 2, 2, 2, 1, 2, 2, 1],
            'Mixolydian': [0, 2, 2, 1, 2, 2, 1, 2],
            'Locrian': [0, 1, 2, 2, 1, 2, 2, 2],
            'Ahava raba': [0, 1, 3, 1, 2, 1, 2, 2],
            'Minor pentatonic': [0, 3, 2, 2, 3, 2],
            'Pentatonic': [0, 2, 2, 3, 2, 3],
            'Blues': [0, 3, 2, 1, 1, 3]
        }

        # Find the index of the given note in the note_order
        note_index = note_order.index(note)

        # Get the intervals for the selected mode
        intervals = mode_dict[mode]

        # Initialize the scale with the starting note
        scale = []

        # Build the scale by applying the intervals
        for interval in intervals[:-1]:  # Exclude the last interval
            note_index = (note_index + interval) % 12
            scale.append(note_order[note_index])

        return scale


class MappingUtils:
    @staticmethod
    def linear_map(value, from_low, from_high, to_low, to_high):
        """
        Linearly maps a value from one range to another.

            Args:
                value (float): The value to be mapped.
                from_low (float): The lower bound of the original range.
                from_high (float): The upper bound of the original range.
                to_low (float): The lower bound of the target range.
                to_high (float): The upper bound of the target range.

            Returns:
                float: The mapped value in the target range.
        """

        return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low


class AudioUtils:
    @staticmethod
    def dataset_to_wav(dataset, output_filename, sample_width=2, sample_rate=44100):
        """
        Convert a dataset of audio samples into a .wav file.

            Args:
                dataset: A list or array of audio samples (e.g., integers or floats).
                output_filename: The name of the .wav file you want to create.
                sample_width: The sample width in bytes (e.g., 1 for 8-bit, 2 for 16-bit). Default is 2.
                sample_rate: The sample rate in Hz (e.g., 44100 for CD-quality audio). Default = 44100.

            Returns:
                None
        """

        # Open a new .wav file for writing
        with wave.open(output_filename, 'w') as wav_file:
            # Set the parameters for the .wav file
            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.setnframes(len(dataset))

            # Write the audio data to the file
            audio_data = array.array('h' if sample_width == 2 else 'b', dataset)
            wav_file.writeframes(audio_data.tobytes())


class ImageUtils:
    @staticmethod
    def get_pixel_positions(image_path: str):
        """
        Method for iterating through every pixel in an image. The iteration is vertical.
        The loop breaks on the first value encountered in a vertical row, because waveforms can only have one y value
        per x.

            Args:
                image_path (str): the path and name of the file to be checked.

            Returns:
                list: all values that can be used in a waveform.
        """

        img = Image.open(image_path)

        result = []

        # Get the dimensions of the image and store for iteration
        width, height = img.size

        # Iterate through each pixel vertically
        for x in range(width):
            for y in range(height):
                # Get the RGB values of the pixel at (x, y)
                pixel = img.getpixel((x, y))

                # If the pixel is not white, store the position of that pixel
                if pixel != (255, 255, 255, 255):
                    y_val = MappingUtils.linear_map(y, 0, height, height, 0)
                    y_val = int(y_val)  # times 4 to make it more distinctive, edit this later.
                    result.append(y_val)
                    break  # makes sure there is only one value per vertical row

        return result


class ChordUtils:
    CHORDS_NOTES_DICT = {
        'C': ['C', 'E', 'G'],
        'C#': ['C#', 'E#', 'G#'],
        'Db': ['Db', 'F', 'Ab'],
        'D': ['D', 'F#', 'A'],
        'D#': ['D#', 'F##', 'A#'],
        'Eb': ['Eb', 'G', 'Bb'],
        'E': ['E', 'G#', 'B'],
        'Fb': ['Fb', 'Ab', 'Cb'],
        'F': ['F', 'A', 'C'],
        'F#': ['F#', 'A#', 'C#'],
        'Gb': ['Gb', 'Bb', 'Db'],
        'G': ['G', 'B', 'D'],
        'G#': ['G#', 'B#', 'D#'],
        'Ab': ['Ab', 'C', 'Eb'],
        'A': ['A', 'C#', 'E'],
        'A#': ['A#', 'C##', 'F'],
        'Bb': ['Bb', 'D', 'F'],
        'B': ['B', 'D#', 'F#'],
        'Cb': ['Cb', 'Eb', 'Gb'],
        'Cm': ['C', 'Eb', 'G'],
        'C#m': ['C#', 'E', 'G#'],
        'Dbm': ['Db', 'E', 'Ab'],
        'Dm': ['D', 'F', 'A'],
        'D#m': ['D#', 'F#', 'A#'],
        'Ebm': ['Eb', 'Gb', 'Bb'],
        'Em': ['E', 'G', 'B'],
        'Fm': ['F', 'Ab', 'C'],
        'F#m': ['F#', 'A', 'C#'],
        'Gbm': ['Gb', 'A', 'Db'],
        'Gm': ['G', 'Bb', 'D'],
        'G#m': ['G#', 'B', 'D#'],
        'Abm': ['Ab', 'B', 'Eb'],
        'Am': ['A', 'C', 'E'],
        'A#m': ['A#', 'C#', 'F'],
        'Bbm': ['Bb', 'Db', 'F'],
        'Bm': ['B', 'D', 'F#'],
        'Cbm': ['Cb', 'Ebb', 'Gbb']
    }


    @staticmethod
    def get_chord_notes(chord: str):
        """
        Returns the chord based on the root note.

            Args:
                chord (str): the root note (like 'A' or 'Bm')

            returns:
                list: all notes within the chord.
        """

        return ChordUtils.CHORDS_NOTES_DICT[chord]

    @staticmethod
    def get_progression(progression: str, note: str, mode: str):
        """
            Generate a chord progression based on a given musical note and mode.

            Parameters:
            - progression (str): A string with the progression. Example: I-V-vi-IV.
            - note (str): The root note of the scale (e.g., 'C', 'D#', 'G').
            - mode (str): The musical mode for the scale (e.g., 'major' or 'minor').

            Returns:
            - chords_list (list): A list of chord names corresponding to the given progression.
        """
        progression = progression.replace('–', '-')

        scale = ScaleUtils.get_scale(note, mode)

        progression = progression.split('-')

        chords_list = []

        for p in progression:
            if p.isupper():
                convert_progression = {
                    'I': 0,
                    'II': 1,
                    'III': 2,
                    'IV': 3,
                    'V': 4,
                    'VI': 5,
                    'VII': 6,
                }
                chord = scale[convert_progression[p]]
            else:
                convert_progression = {
                    'i': 0,
                    'ii': 1,
                    'iii': 2,
                    'iv': 3,
                    'v': 4,
                    'vi': 5,
                    'vii': 6,
                }

                chord = str(scale[convert_progression[p]]) + 'm'

            chords_list.append(chord)

        return chords_list


class MidiUtils:
    PITCHES = {
        'A': 57,
        'A#': 58,
        'Bb': 58,
        'B': 59,
        'C': 60,
        'C#': 61,
        'Db': 61,
        'D': 62,
        'D#': 63,
        'Eb': 63,
        'E': 64,
        'F': 65,
        'F#': 66,
        'Gb': 66,
        'G': 67,
        'G#': 68,
        'Ab': 68
    }

    @staticmethod
    def get_chord_note_pitch(note: str):
        """
        Retrieve MIDI pitch values for a given musical note.

        Parameters:
        - note (str): The musical note for which the MIDI pitch value is needed (e.g., 'C', 'D#', 'G').

        Returns:
        - pitches (list): A list of MIDI pitch values corresponding to the input note.
        """

        return MidiUtils.PITCHES[note]
