import fractions
import random
from tensorflow import keras
import pickle
import os
import numpy as np
from datetime import datetime
import lilypond_utilities
from lilypond_utilities import translate_write_empty, translate_key_lilypond, translate_tempo


class Engine:
    pitch_dict_reversed = []
    rhythm_dict_reversed = []
    pitch_input_seq = []
    rhythms_input_seq = []

    model = keras.models.load_model('backup\\3-4_11-15-2022_14-22_mine_3-4\\model\\my_model')

    def __init__(self):
        print("hi")
        backup_training_set_folder = 'backup/3-4_11-15-2022_14-22_mine_3-4/training_set_backup'
        seq_len = 12

        # Reading previously saved information about training data
        with open(os.path.join(backup_training_set_folder, 'dictionaries'), 'rb') as file:
            pitch_sorted, pitch_dict, rhythm_sorted, rhythm_dict, Engine.pitch_dict_reversed, \
                Engine.rhythm_dict_reversed = pickle.load(file)

        pitch_input = ['S'] * seq_len
        rhythm_input = [0.0] * seq_len

        for p, r in zip(pitch_input, rhythm_input):  # translating into numbers
            Engine.pitch_input_seq.append(pitch_dict[p])
            Engine.rhythms_input_seq.append(rhythm_dict[r])

        print(rhythm_dict)
        print(pitch_dict)

    @staticmethod
    def generate(temperature, number_of_bars):
        """ Here is where the magic happens - generating using previously created neural network """

        time_sig = "3/4"
        time_signature = time_sig.split("/")
        upper_numeral = int(time_signature[0])
        lower_numeral = 1.0  # quarter note

        desired_length = number_of_bars * upper_numeral * lower_numeral  # how long should the dictation be?
        actual_length = 0.0

        # Generating new dictation =====================================================================================
        # Final generated melody and rhythm
        pitch_final_prediction = []
        rhythm_final_prediction = []

        # Arrays which are going to be an input in neural network model, we will keep updating them at each time step
        pitch_inseq = Engine.pitch_input_seq.copy()
        rhythm_inseq = Engine.rhythms_input_seq.copy()

        while actual_length < desired_length:
            # Generate the arrays of probability what the next note will be
            prediction_in = [np.array([pitch_inseq]), np.array([rhythm_inseq])]
            pitch_prediction, rhythm_prediction = Engine.model.predict(prediction_in, verbose=0)

            # Sample with temperature to choose new rhythm and pitch
            chosen_pitch = temperature_sampling(pitch_prediction[0], temperature)
            chosen_rhythm = temperature_sampling(rhythm_prediction[0], temperature)

            # Append new pitch and rhythm, and get rid of the oldest one in the sequence (first)
            pitch_inseq.append(chosen_pitch)
            pitch_inseq = pitch_inseq[1:]
            rhythm_inseq.append(chosen_rhythm)
            rhythm_inseq = rhythm_inseq[1:]

            # Translate chosen pitch and rhythm to its name and add those to generated melody
            pitch_to_name = Engine.pitch_dict_reversed[chosen_pitch]
            rhythm_to_name = Engine.rhythm_dict_reversed[chosen_rhythm]
            pitch_final_prediction.append(pitch_to_name)
            rhythm_final_prediction.append(rhythm_to_name)

            # Update current length of generated melody ================================================================
            # triplet - this generates some problems with number precision, I take care of that later
            if rhythm_to_name == fractions.Fraction(1, 3):
                actual_length += 0.3333  #

            # dotted half note - it's a fix for the non-precise read of the midi files
            elif rhythm_to_name == 2.75:
                actual_length += 3.0

            else:
                actual_length += round(rhythm_to_name * 4) / 4

        # If generated dictation is too long ===========================================================================
        actual_length = (round(actual_length * 4) / 4)
        if actual_length != desired_length:
            last_rhythm = rhythm_final_prediction[-1]
            rhythm_final_prediction.pop()  # deleting last rhythm
            missing_time = desired_length - (actual_length - last_rhythm)  # how much time to fill the bars is missing?

            if missing_time != 0.0:
                rhythm_final_prediction.append(missing_time)

        return pitch_final_prediction, rhythm_final_prediction

    def save_file(self, pitch_final_prediction, rhythm_final_prediction, input_path, key_sig_str, tempo_str,
                  write_midi, write_empty, hints):
        """ Executing all the other functions that help to format and execute written files """

        # Generate the melody
        lily_melody = translate_melody_to_lily(pitch_final_prediction, rhythm_final_prediction)

        # Format the file to lilypond acceptable format and execute it
        my_template, path_to_save = self.format_file(lily_melody, key_sig_str, tempo_str,
                                                     write_empty=False, hints=0)
        execute_lilypond(my_template, input_path, path_to_save, midi_save=write_midi)

        # If user chose to generate empty file as well
        if write_empty:
            empty_template, path_to_save_empty = self.format_file(lily_melody, key_sig_str,
                                                                  tempo_str, write_empty=True, hints=hints)
            execute_lilypond(empty_template, input_path, path_to_save_empty, midi_save=False)

    @staticmethod
    def format_file(generated_string, key_signature, tempo, write_empty, hints):
        """ Saving file to the LilyPond .ly format and then executing it to get PDF and MIDI files. """

        # Prepare all the parameters to fit Lilypond notation
        date_title = str(datetime.now().strftime("Wygenerowano %m.%d.%Y o godzinie %H:%M"))
        tempo = translate_tempo(tempo)
        key_signature = translate_key_lilypond(key_signature)
        time_signature = "3/4"  # TODO - input here if creating dictations in more time signatures
        beats_per_measure = prepare_beats_midi(time_signature)
        write_empty_text = translate_write_empty(write_empty)

        # Prepare the melody
        first_note = generated_string[0]  # First note will ALWAYS show
        generated_string = show_random(generated_string, number_of_hints=hints)
        generated_melody = "\n".join(generated_string[1:])

        # Prepare filepaths to save output files
        date = str(datetime.now().strftime("%m-%d-%Y_%H-%M"))
        if not write_empty:
            filename_to_save = "dictation_" + date + ".ly"
        else:
            filename_to_save = "dictation_" + date + "_empty.ly"

        # Main template of LilyPond dictation
        my_template = """\\version "2.22.2"
                \\paper {{#(set-paper-size "a4")}}
                \\header {{
                    title = "Nutomat"
                    subtitle = " {date_title} "
                }}
                myMusic = {{
                    \\new Staff {{
                        \\set Staff.midiInstrument = "acoustic grand"
                        \\numericTimeSignature
                        
                        \\key {key_signature} \\major
                        \\new Voice \\with {{
                            \\remove Note_heads_engraver
                            \\consists Completion_heads_engraver
                        }}
                        \\time {time_signature}
                        \\tag #'midionly {{
                            \\tempo 4 = {tempo}
                                {beats_per_measure}
                            }}
                        \\transpose c {key_signature} {{
                            \\omit TupletNumber
                            {first_note}
                            {write_empty_text}
                            {generated_melody}
                        }}
                        \\bar "|."
                    }}
                }}

                \\score {{
                    \\removeWithTag #'midionly
                    \\myMusic
                    \\layout {{}}
                }} """.format(date_title=date_title,
                              tempo=tempo,
                              key_signature=key_signature,
                              time_signature=time_signature,
                              beats_per_measure=beats_per_measure,
                              first_note=first_note,
                              write_empty_text=write_empty_text,
                              generated_melody=generated_melody)

        return my_template, filename_to_save


def show_random(generated_string, number_of_hints):
    """ Function that helps create random visible notes when user has chosen to get hints """

    if number_of_hints == 0:
        return generated_string

    hide = "\\hideNotes"
    un_hide = "\\unHideNotes"
    random_places = random.sample(range(len(generated_string)), number_of_hints)
    randomized_melody = []

    for index, value in enumerate(generated_string):
        # If the index of the note got selected in random.sample, then wrap it in un_hide and hide again

        # "Before wrap"
        if index in random_places:
            randomized_melody.append(un_hide)

        # This always happens
        randomized_melody.append(value)

        # "After wrap"
        if index in random_places:
            randomized_melody.append(hide)

    return randomized_melody


def translate_melody_to_lily(pitch_final_prediction, rhythm_final_prediction):
    return lilypond_utilities.music21_to_lily(pitch_final_prediction, rhythm_final_prediction)


def prepare_beats_midi(time_signature):
    """ Prepares a measure of quarter notes - first bear of beats - useful in audio/midi files when
    solving a musical dictation """
    return ("g" + time_signature.partition("/")[2] + " ") * int(time_signature.partition("/")[0])


def temperature_sampling(predictions, temp):
    if temp == 0:
        return np.argmax(predictions)
    else:
        predictions = np.log(predictions) / temp
        exp_predictions = np.exp(predictions)
        predictions = exp_predictions / np.sum(exp_predictions)
        return np.random.choice(len(predictions), p=predictions)


def execute_lilypond(template, input_path, filename_to_save, midi_save):
    """ Creating lilypond files and executing them """

    if not os.path.exists(os.path.join(input_path, 'LilyPond')):
        os.mkdir(os.path.join(input_path, 'LilyPond'))

    lilypond_folder = os.path.join(input_path, 'LilyPond')
    lilypond_filename = os.path.join(lilypond_folder, filename_to_save)

    # If user has chosen to generate .MID file as well
    midi = """\\score {
        \\myMusic
        \\midi {}
    }"""

    with open(lilypond_filename, 'w') as dictation_file:
        dictation_file.write(template)
        if midi_save:
            dictation_file.write(midi)

    # Execute the lilypond file
    command = 'lilypond.exe -o "' + input_path + '" "' + lilypond_filename + '"'
    os.system(command)


def hints_count(switch_hints, number_of_bars):
    if switch_hints == 1 and number_of_bars == 2:
        hints = 2
    elif switch_hints == 1 and number_of_bars == 4:
        hints = 4
    elif switch_hints == 1 and number_of_bars == 8:
        hints = 6
    elif switch_hints == 1 and number_of_bars == 16:
        hints = 8
    else:
        hints = 0

    return hints
