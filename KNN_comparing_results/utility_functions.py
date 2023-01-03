# Method for translating the dictations and/or shortening them to 15 notes
def translate(dictations, pitches):
    short_dictations = []
    for dictation in dictations:
        translated = []
        if pitches:
            for note in dictation[0:14]:
                translated.append(melody_translator_numbers(note))
        else:
            translated = dictation[0:14]

        short_dictations.append(translated)

    return short_dictations


# Method that will translate pitches into floats
def melody_translator_numbers(music21_notation):
    switcher = {
        "rest": -10,

        "C3": 1,
        "C#3": 1.25,
        "D-3": 1.75,
        "D3": 2,
        "D#3": 2.25,
        "E-3": 2.75,
        "E3": 3,
        "E#3": 3.25,
        "F-3": 3.75,
        "F3": 4,
        "F#3": 4.25,
        "G-3": 4.75,
        "G3": 5,
        "G#3": 5.25,
        "A-3": 5.75,
        "A3": 6,
        "A#3": 6.25,
        "B-3": 6.75,
        "B3": 7,
        "B#3": 7.25,

        "C4": 11,
        "C#4": 11.25,
        "D-4": 11.75,
        "D4": 12,
        "D#4": 12.25,
        "E-4": 12.75,
        "E4": 13,
        "E#4": 13.25,
        "F-4": 13.75,
        "F4": 14,
        "F#4": 14.25,
        "G-4": 14.75,
        "G4": 15,
        "G#4": 15.25,
        "A-4": 15.75,
        "A4": 16,
        "A#4": 16.25,
        "B-4": 16.75,
        "B4": 17,
        "B#4": 17.25,

        "C5": 21,
        "C#5": 21.25,
        "D-5": 21.75,
        "D5": 22,
        "D#5": 22.25,
        "E-5": 22.75,
        "E5": 23,
        "E#5": 23.25,
        "F-5": 23.75,
        "F5": 24,
        "F#5": 24.25,
        "G-5": 24.75,
        "G5": 25,
        "G#5": 25.25,
        "A-5": 25.75,
        "A5": 26,
        "A#5": 26.25,
        "B-5": 26.75,
        "B5": 27,
        "B#5": 27.25,

        "C6": 31,
        "C#6": 31.25,
        "D-6": 31.75,
        "D6": 32,
        "D#6": 32.25,
        "E-6": 32.75,
        "E6": 33,
        "E#6": 33.25,
        "F-6": 33.75,
        "F6": 34,
        "F#6": 34.25,
        "G-6": 34.75,
        "G6": 35,
        "G#6": 35.25,
        "A-6": 35.75,
        "A6": 36,
        "A#6": 36.25,
        "B-6": 36.75,
        "B6": 37,
        "B#6": 37.25,

        "C7": 41,
        "C#7": 41.25,
        "D-7": 41.75,
        "D7": 42,
        "D#7": 42.25,
        "E-7": 42.75,
        "E7": 43,
        "E#7": 43.25,
        "F-7": 43.75,
        "F7": 44,
        "F#7": 44.25,
        "G-7": 44.75,
        "G7": 45,
        "G#7": 45.25,
        "A-7": 45.75,
        "A7": 46,
        "A#7": 46.25,
        "B-7": 46.75,
        "B7": 47,
        "B#7": 47.25,
    }

    if switcher.get(music21_notation) is None:
        return 11.0
    else:
        return float(switcher.get(music21_notation))