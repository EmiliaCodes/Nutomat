#  Nutomat
This project allows you to prepare your own neural network which will use MIDI files with melodies as a training set and later will allows you to create new melodic dictations and then save it in **PDF** and **MIDI** format. In this project I am using *music21* and *keras* libraries. *LilyPond* is used for creating PDF and MIDI files with generated output. 

It consists of user interface that helps with easy interactions. It is possible to change the **length of dictation (in bars**), its **key signature**, the **tempo** of the generated MIDI file and the path where the files will be saved. In the default, the app generates PDF file with the melody using LilyPond. The UI also lets the user to choose whether or not they want to generate MIDI file with the new melody, and a PDF file that would be helpful in solving a musical dictation - empty music staff with first note shown as the default (and some extra visible "hint notes" if the toggle with hints is on). 

:bulb: <sub> The code generates a PDF version of the dictation and MIDI version. In the MIDI version, as it is intended to be played *(and possibly later in the project development changed into some actual audio format like WAVE or MP3)*, you will hear an additional "empty bar" at the beginning of the dictation - a measure with basic rhythm values specific for this particular time signature (eg. three quarter notes in 3/4 time signature). </sub>

## Structure of the project
The code consists of two main parts:
  1. **Preparing the training set and the neural network** - [Przygotowanie_sieci.ipynb](Przygotowanie_sieci.ipynb). This is a script created with jupyter notebook that prepares MIDI training set files, the network itself, trains the network and saves the output to be later loaded by the UI part of the system.
  2. **User interface** - this part allows to use previously prepared neural network and generate new melodies. Consists of a couple of files:
      - [main.py](main.py) - starting the app
      - [GUI.py](GUI.py) - creating and managing the graphical user interface. The engine part is called in [generate()](GUI.py)


## Running the code
If you want to try out and run this code you will have to install [LilyPond](https://lilypond.org/). If you will encounter any problems, make sure the folder with LilyPond is added to PATH in your system enviornment variables.



## Examples

