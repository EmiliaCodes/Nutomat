import fractions
import random
import pickle
import os
import numpy as np
from datetime import datetime
import lilypond_utilities
from lilypond_utilities import translate_write_empty, translate_key_lilypond, translate_tempo
import model_architecture


class Engine:
    model_44 = None
    model_34 = None
    pitch_dict_reversed34 = []
    rhythm_dict_reversed34 = []
    pitch_input_seq34 = []
    rhythms_input_seq34 = []
    pitch_dict_reversed44 = []
    rhythm_dict_reversed44 = []
    pitch_input_seq44 = []
    rhythms_input_seq44 = []

    def __init__(self):

        # Path with backup and model of 3/4 dictations
        path34 = '3-4_with-attention_11-30-2022_08-34'

        # Path with backup and model of 4/4 and 2/4 dictations
        path44 = '4-4_with-attention_11-29-2022_20-13'

        path34_training_set = os.path.join(path34, 'training_set_backup')
        path44_training_set = os.path.join(path44, 'training_set_backup')

        path34_weights = os.path.join(path34, 'model\\weights.h5')
        path44_weights = os.path.join(path44, 'model\\weights.h5')

        backup_training_set_folder34 = path34_training_set
        backup_training_set_folder44 = path44_training_set

        seq_len = 10

        # Reading previously saved information about training data
        with open(os.path.join(backup_training_set_folder34, 'dictionaries'), 'rb') as file:
            pitch_sorted, pitch_dict34, rhythm_sorted, rhythm_dict34, Engine.pitch_dict_reversed34, \
            Engine.rhythm_dict_reversed34 = pickle.load(file)

        with open(os.path.join(backup_training_set_folder44, 'dictionaries'), 'rb') as file:
            pitch_sorted, pitch_dict44, rhythm_sorted, rhythm_dict44, Engine.pitch_dict_reversed44, \
            Engine.rhythm_dict_reversed44 = pickle.load(file)

        pitch_input = ['S'] * seq_len
        rhythm_input = [0.0] * seq_len

        for p, r in zip(pitch_input, rhythm_input):  # translating into numbers
            Engine.pitch_input_seq34.append(pitch_dict34[p])
            Engine.rhythms_input_seq34.append(rhythm_dict34[r])
            Engine.pitch_input_seq44.append(pitch_dict44[p])
            Engine.rhythms_input_seq44.append(rhythm_dict44[r])

        Engine.model_34 = model_architecture.create_model(rhythm_dict34, pitch_dict34, path34_weights)
        Engine.model_44 = model_architecture.create_model(rhythm_dict44, pitch_dict44, path44_weights)

    @staticmethod
    def generate(temperature, number_of_bars, time_sig):
        """ Generating using previously created neural network """

        time_signature = time_sig.split("/")
        upper_numeral = int(time_signature[0])
        lower_numeral = 1.0  # quarter note

        # how long should the dictation be
        desired_length = number_of_bars * upper_numeral * lower_numeral

        # length of the dictation - updated at each time step
        actual_length = 0.0

        # Generating new dictation =====================================================================================
        # Final generated melody and rhythm
        pitch_final_prediction = []
        rhythm_final_prediction = []

        if time_sig == "3/4":
            model = Engine.model_34
            pitch_inseq = Engine.pitch_input_seq34.copy()
            rhythm_inseq = Engine.rhythms_input_seq34.copy()
            pitch_dict_reversed = Engine.pitch_dict_reversed34
            rhythm_dict_reversed = Engine.rhythm_dict_reversed34

        else:  # 4/4
            model = Engine.model_44
            pitch_inseq = Engine.pitch_input_seq44.copy()
            rhythm_inseq = Engine.rhythms_input_seq44.copy()
            pitch_dict_reversed = Engine.pitch_dict_reversed44
            rhythm_dict_reversed = Engine.rhythm_dict_reversed44

        # Loop for generating
        while actual_length < desired_length:
            # Generate the arrays of probability what the next note will be
            prediction_in = [np.array([pitch_inseq]), np.array([rhythm_inseq])]

            pitch_prediction, rhythm_prediction = model.predict(prediction_in, verbose=0)

            # Sample with temperature to choose new rhythm and pitch
            chosen_pitch = temperature_sampling(pitch_prediction[0], temperature)
            chosen_rhythm = temperature_sampling(rhythm_prediction[0], temperature)

            # Append new pitch and rhythm, and get rid of the oldest one in the sequence (first)
            pitch_inseq.append(chosen_pitch)
            pitch_inseq = pitch_inseq[1:]
            rhythm_inseq.append(chosen_rhythm)
            rhythm_inseq = rhythm_inseq[1:]

            # Translate chosen pitch and rhythm to its name and add those to generated melody
            pitch_to_name = pitch_dict_reversed[chosen_pitch]
            rhythm_to_name = rhythm_dict_reversed[chosen_rhythm]
            pitch_final_prediction.append(pitch_to_name)
            rhythm_final_prediction.append(rhythm_to_name)

            # Update current length of generated melody ============
            # triplet - this generates some problems with number precision, I take care of that later
            if rhythm_to_name == fractions.Fraction(1, 3):
                actual_length += 0.3333  #

            else:
                actual_length += round(rhythm_to_name * 4) / 4

            if rhythm_to_name == -1.0:
                break

        # ==============================================================================================================

        # If generated dictation is too long ===========================================================================
        actual_length = (round(actual_length * 4) / 4)

        if actual_length != desired_length:
            last_rhythm = rhythm_final_prediction[-1]
            rhythm_final_prediction.pop()  # deleting last rhythm
            missing_time = desired_length - (actual_length - last_rhythm)  # how much time to fill the bars

            if missing_time != 0.0:
                rhythm_final_prediction.append(missing_time)

        return pitch_final_prediction, rhythm_final_prediction

    def save_file(self, pitch_final_prediction, rhythm_final_prediction, input_path, key_sig_str, tempo_str,
                  write_midi, write_empty, hints, time_sig):
        """ Executing all the other functions that help to format and execute written files """

        # Generate the melody, translate to LilyPond notation
        lily_melody = lilypond_utilities.music21_to_lily(pitch_final_prediction, rhythm_final_prediction)

        # Format the file to lilypond acceptable format and execute it
        my_template, path_to_save = self.format_file(lily_melody, key_sig_str, tempo_str, time_sig,
                                                     write_empty=False, hints=0)
        execute_lilypond(my_template, input_path, path_to_save, midi_save=write_midi)

        # If user chose to generate empty file as well
        if write_empty:
            empty_template, path_to_save_empty = self.format_file(lily_melody, key_sig_str,
                                                                  tempo_str, time_sig, write_empty=True, hints=hints)
            execute_lilypond(empty_template, input_path, path_to_save_empty, midi_save=False)

    @staticmethod
    def format_file(generated_string, key_signature, tempo, time_sig, write_empty, hints):
        """ Saving file to the LilyPond .ly format and then executing it to get PDF and MIDI files. """

        # Prepare all the parameters to fit Lilypond notation
        date_title = str(datetime.now().strftime("Wygenerowano %d.%m.%Y o godzinie %H:%M"))
        tempo = translate_tempo(tempo)
        key_signature = translate_key_lilypond(key_signature)
        time_signature = time_sig
        beats_per_measure = prepare_beats_midi(time_signature)
        write_empty_text = translate_write_empty(write_empty)

        # Prepare the melody
        first_note = generated_string[0]  # First note will ALWAYS show
        generated_string = show_random(generated_string, number_of_hints=hints)
        generated_melody = "\n".join(note for note in generated_string[1:] if note is not None)

        # Prepare filepaths to save output files
        date = str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        if not write_empty:
            filename_to_save = "dictation_" + date + ".ly"
        else:
            filename_to_save = "dictation_" + date + "_empty.ly"

        # Main template of LilyPond dictation
        my_template = """\\version "2.22.2"
                \\paper {{
                    #(set-paper-size "a4")
                    markup-system-spacing =
                        #'((basic-distance . 15)
                            (minimum-distance . 6)
                            (padding . 1)
                            (stretchability . 12)
                           )
                }}
                \\header {{
                    title = "Nutomat"
                    subtitle = " {date_title} "
                }}
                myMusic = {{
                    \\new Staff {{
                        \\set Staff.midiInstrument = "acoustic grand"
                        \\numericTimeSignature
                        
                        \\new Voice \\with {{
                            \\remove "Note_heads_engraver"
                            \\consists "Completion_heads_engraver"
                            \\remove "Rest_engraver"
                            \\consists "Completion_rest_engraver"
                        }}

                        \\time {time_signature}
                        \\key {key_signature} \\major
                        \\tag #'midionly {{
                            \\tempo 4 = {tempo}
                            \\transpose c {key_signature} {{
                                {beats_per_measure}
                            }}
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
                    \\layout {{
                            \\context {{
                                \\Score
                                    \\override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
                            }}
                    }}
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
    un_hide = "\\unHideNotes \\hide Stem"
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


def prepare_beats_midi(time_signature):
    """ Prepares a measure of quarter notes - first bear of beats - useful in audio/midi files when
    solving a musical dictation """
    cadenza = """<c' e' g'> 4
        <c' f' a'> 4
        <b d' g'> 4
        <c' e' g'> 2. """
    if time_signature.partition("/")[0] == "4":  # if 4/4 fill the bar with rest
        cadenza += "r 2"

    return cadenza


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
    command = 'LilyPond\\usr\\bin\\lilypond.exe -o "' + input_path + '" "' + lilypond_filename + '"'
    os.system(command)


def hints_count(switch_hints, number_of_bars):
    if switch_hints == 1 and number_of_bars == 4:
        hints = 4
    elif switch_hints == 1 and number_of_bars == 8:
        hints = 6
    elif switch_hints == 1 and number_of_bars == 12:
        hints = 8
    elif switch_hints == 1 and number_of_bars == 16:
        hints = 10
    else:
        hints = 0

    return hints
