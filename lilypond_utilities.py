from fractions import Fraction


def music21_to_lily(pitch_final_prediction, rhythm_final_prediction):
    """ Function that translates music21 notation to lilypond format"""

    lily_notation = []
    for i, (note_pitch, note_rhythm) in enumerate(zip(pitch_final_prediction, rhythm_final_prediction)):
        # This "if" is an error fix - music21 tends to read dotted half note as a 2.75 and then 0.25. This ensures
        # we translate 2.75 as a dotted half note and skip the next note which is a rest anyway
        if i != 0 and note_rhythm == 0.25 and rhythm_final_prediction[i - 1] == 2.75:
            continue

        # Skip the loop accidentally we got the starting mark
        if note_pitch == 'S':
            continue

        this_pitch = melody_translator(note_pitch)
        lily_notation.append(rhythm_translator(note_rhythm, this_pitch))

    return lily_notation


def melody_translator(music21_notation):
    """ Manual conversion of music21 pitch to lilypond. There are built-in translators in music21 library, but
    they do have problems when it comes to translating triplets, so I solved it translating manually"""

    switcher = {
        "rest": "r",
        "C3": "c",
        "C#3": "cis",
        "D-3": "des",
        "D3": "d",
        "D#3": "dis",
        "E-3": "es",
        "E3": "e",
        "E#3": "eis",
        "F-3": "fes",
        "F3": "f",
        "F#3": "fis",
        "G-3": "ges",
        "G3": "g",
        "G#3": "gis",
        "A-3": "as",
        "A3": "a",
        "A#3": "ais",
        "B-3": "bes",
        "B3": "b",
        "B#3": "bis",

        "C4": "c'",
        "C#4": "cis'",
        "D-4": "des'",
        "D4": "d'",
        "D#4": "dis'",
        "E-4": "es'",
        "E4": "e'",
        "E#4": "eis'",
        "F-4": "fes'",
        "F4": "f'",
        "F#4": "fis'",
        "G-4": "ges'",
        "G4": "g'",
        "G#4": "gis'",
        "A-4": "as'",
        "A4": "a'",
        "A#4": "ais'",
        "B-4": "bes'",
        "B4": "b'",
        "B#4": "bis'",

        "C5": "c''",
        "C#5": "cis''",
        "D-5": "des''",
        "D5": "d''",
        "D#5": "dis''",
        "E-5": "es''",
        "E5": "e''",
        "E#5": "eis''",
        "F-5": "fes''",
        "F5": "f''",
        "F#5": "fis''",
        "G-5": "ges''",
        "G5": "g''",
        "G#5": "gis''",
        "A-5": "as''",
        "A5": "a''",
        "A#5": "ais''",
        "B-5": "bes''",
        "B5": "b''",
        "B#5": "bis''",

        "C6": "c'''",
        "C#6": "cis'''",
        "D-6": "des'''",
        "D6": "d'''",
        "D#6": "dis'''",
        "E-6": "es'''",
        "E6": "e'''",
        "E#6": "eis'''",
        "F-6": "fes'''",
        "F6": "f'''",
        "F#6": "fis'''",
        "G-6": "ges'''",
        "G6": "g'''",
        "G#6": "gis'''",
        "A-6": "as'''",
        "A6": "a'''",
        "A#6": "ais'''",
        "B-6": "bes'''",
        "B6": "b'''",
        "B#6": "bis'''",

        "C7": "c''''",
        "C#7": "cis''''",
        "D-7": "des''''",
        "D7": "d''''",
        "D#7": "dis''''",
        "E-7": "es''''",
        "E7": "e''''",
        "E#7": "eis''''",
        "F-7": "fes''''",
        "F7": "f''''",
        "F#7": "fis''''",
        "G-7": "ges''''",
        "G7": "g''''",
        "G#7": "gis''''",
        "A-7": "as''''",
        "A7": "a''''",
        "A#7": "ais''''",
        "B-7": "bes''''",
        "B7": "b''''",
        "B#7": "bis''''",
    }
    return switcher.get(music21_notation)


def rhythm_translator(music21_notation, pitch):
    """ Function that translates given rhythm and already translated pitch to lilypond acceptable format """

    switcher = {
        0.0: "",  # none - it's a starting mark anyway, could probably delete that line
        0.25: "{pitch} 16".format(pitch=pitch),  # szesnastka
        Fraction(1, 3): "\\tuplet 3/2 {{ {pitch} 8 }}".format(pitch=pitch),  # triola
        0.5: "{pitch} 8".format(pitch=pitch),  # ósemka
        0.75: "{pitch} 8.".format(pitch=pitch),  # ósemka z kropką
        1.0: "{pitch} 4".format(pitch=pitch),  # ćwierćnuta
        1.5: "{pitch} 4.".format(pitch=pitch),  # ćwierćnuta z kropką
        2.0: "{pitch} 2".format(pitch=pitch),  # półnuta
        2.75: "{pitch} 2.".format(pitch=pitch)  # półnuta z kropką
    }
    return switcher.get(music21_notation)


def translate_write_empty(write_empty):
    if write_empty:
        return "\\hideNotes"
    else:
        return ""


def translate_key_lilypond(argument):
    switcher = {
        "C": "c",
        "F": "f",
        "G": "g",
        "B": "bes",
        "D": "d",
    }
    return switcher.get(argument)


def translate_tempo(tempo_str):
    switcher = {
        "szybkie": "120",
        "umiarkowane": "90",
        "wolne": "60"
    }
    return switcher.get(tempo_str)
