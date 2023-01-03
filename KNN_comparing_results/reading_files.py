import os
from music21 import converter, chord, key, interval, pitch
import pickle


# Reading and saving info from files in the training sets ============
# Reading training set
source_folder = 'D:/Studia/Praca_inzynierska/Baza_dyktanda/Lasocki_solfez/3-4/MIDI/'
# source_folder = 'D:/Studia/Praca_inzynierska/Baza_dyktanda/Lasocki_solfez/4-4/MIDI/'

save_to = 'D:\\Studia\\praca-python\\nneighbors\\3_4-kneighbors'
# save_to = 'D:\\Studia\\praca-python\\nneighbors\\4_4-kneighbors'

files = os.listdir(source_folder)
pitch_read = []
rhythm_read = []

pitch_input = []
pitch_output = []
rhythm_input = []
rhythm_output = []

pitch_input_encoded = []
pitch_output_encoded = []
rhythm_input_encoded = []
rhythm_output_encoded = []

all_lengths = []
all_rhythms = []
filenames = []

for file in files:
    filenames.append(str(file))

    pitch_this_file = []
    rhythm_this_file = []

    dictation = converter.parse(source_folder + file)

    # Transpose to C-major
    dictation_key_signature = dictation.analyze('key')

    if dictation_key_signature != key.Key('C'):
        i = interval.Interval(dictation_key_signature.tonic, pitch.Pitch('C'))
        dictation = dictation.transpose(i)

    part_stream = dictation.parts.stream()
    my_part = part_stream[0]  # ensuring we will use only the top melody IF we had multi-melody training set pieces

    for element in my_part.flat.notesAndRests:
        if element.isNote:
            pitch_this_file.append(str(element.nameWithOctave))
            rhythm_this_file.append(element.duration.quarterLength)

        if element.isRest:
            pitch_this_file.append(str(element.name))  # 'rest'
            rhythm_this_file.append(element.duration.quarterLength)

        if isinstance(element, chord.Chord):  # if chord insert only the highest note
            pitch_this_file.append(element.pitches[-1].nameWithOctave)
            rhythm_this_file.append(element.duration.quarterLength)

    # Adding notes to an array of all the notes
    pitch_read.append(pitch_this_file)
    rhythm_read.extend(rhythm_this_file)


# Saving all necessary data
with open(os.path.join(save_to, 'filenames'), 'wb') as file:
    pickle.dump(filenames, file)

with open(os.path.join(save_to, 'read_melodies'), 'wb') as file:
    pickle.dump(pitch_read, file)

with open(os.path.join(save_to, 'read_rhythm'), 'wb') as file:
    pickle.dump(rhythm_read, file)


