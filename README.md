#  Nutomat
This project allows you to prepare your own neural network which will use MIDI files with melodies as a training set and later will allows you to create new melodic dictations and then save it in PDF and MIDI format. In this project I am using music21 and keras libraries. LilyPond is used for creating PDF and MIDI files with generated output. 

It consists of user interface that helps with easy interactions. 

This project focuses on generating rhythmic dictations using ***Markov Chains***. Using **Java**, it calculates needed matrices based on training files in **MIDI** format, saves read info in .txt file which can be read and used later. After that it generates given set of rhythms and using **LilyPond** saves it in **PDF and MIDI** formats.

It is possible to change length of dictation (in bars), 
## Structure of the project

:bulb: <sub> The code generates a PDF version of the dictation and MIDI version. In the MIDI version, as it is intended to be played *(and possibly later in the project development changed into some actual audio format like WAVE or MP3)*, you will find/hear additional "empty bar" at the beginning of the dictation - a bar with basic rhythm values specific for chosen time signature (eg. four quarter notes in 4/4 time signature). </sub>

## Running the code
If you want to try out and run this code you will have to install [LilyPond](https://lilypond.org/). If you will encounter any problems, make sure the folder with LilyPond is added to PATH in your system enviornment variables.



## Examples

