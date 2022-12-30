#  Nutomat 🎶
This project allows to prepare a neural network which generates new melodies. It uses MIDI files as the training set. Newly generated output can be saved in **PDF** and **MIDI** format. In this project I am using *music21* and *keras* libraries. *LilyPond* is used for creating PDF and MIDI files with generated output. 

The app consists of a user interface that allows for easy interactions. It is possible to change the **length of dictation (in bars**), its **key signature**, the **tempo** of the generated MIDI file and the **path** where the files will be saved.

In the default, the app generates PDF file with the melody using LilyPond. The UI also lets the user to choose whether or not they want to generate MIDI file with the new melody, and a PDF file that would be helpful in using the melody as a musical dictation - empty music staff with only the first note of the melody visible (and some extra visible "hint notes" if the hints toggle is on). 

:bulb: <sub> The code generates a PDF version of the dictation and MIDI version. In the MIDI version, as it is intended to be played *(and possibly later in the project development changed into some actual audio format like WAVE or MP3)*, you will hear an additional "empty bar" at the beginning of the dictation - a measure with basic rhythm values specific for this particular time signature (eg. three quarter notes in 3/4 time signature). </sub>

## Structure of the project
The code consists of two main parts:
  1. **Preparing the training set and the neural network** - [Przygotowanie_sieci.ipynb](Przygotowanie_sieci.ipynb). This is a script created with jupyter notebook that prepares MIDI training set files, the network itself, trains the network and saves the output to be later loaded by the UI part of the system.
  2. **User interface** - this part allows to use previously prepared neural network and generate new melodies with it. Consists of a couple of files:
      - [main.py](main.py) - starting the app
      - [GUI.py](GUI.py) - creating and managing the graphical user interface. The engine part is called in [generate()](GUI.py#L154).
      - [engine.py](engine.py) - heart of the app. Used for generating new melodies and saving them into LilyPond, PDF and MIDI files. The generating part happens [here - generate()](engine.py#L41) while the saving part [here - save_file()](engine.py#L106)
      - [lilypond_utilities.py](lilypond_utilities.py) - used mostly for translating music21 music language into LilyPond supported format.

## Running the code
If you want to try out and run this code you will have to download [LilyPond](https://lilypond.org/) and insert the whole folder inside the Nutomat project folder.

Other additional python dependencies are listed in [requirements file](other/requirements.txt):
```
customtkinter==4.6.3
Keras==2.2.4
music21==5.5.0
numpy==1.16.1
tensorflow==1.14.0
```
:bulb: <sub> I did encounter some problems using Python 3.10, so preferred versions are 3.9 and older. </sub>

## Examples
I am in the mids of creating bigger training set database with 3/4 and 4/4 dictations, but in the meantime you can play with the app using 50 MIDI files in 3/4 signature in [MIDI_3-4](MIDI_3-4/).

If you will train your own network and you want to use other model, you will need to update the path in two places in the [engine.py](engine.py) - [here](engine.py#L18) and [here](engine.py#L22). Otherwise you should be free to play with it just running the [main.py](main.py).

<img src="other/images/example_screen.png" width=50% height=50%>



