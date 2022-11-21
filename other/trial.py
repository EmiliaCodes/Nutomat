import subprocess
import sys
import os

# result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
# print(result.stdout.decode('utf-8'))
# input_path = '"D:/probny folder"'
# lilypond_filename = '"D:/dictation_11-16-2022_11-39.ly"'
input_path = "D:/probny folder"
lilypond_filename = "D:/probny folder/dictation_11-15-2022_15-51.ly"

command = 'lilypond.exe -o "' + input_path + '" "' + lilypond_filename + '"'
command2 = ["lilypond.exe", "-o ", input_path, lilypond_filename]
# os.system(command)
result = subprocess.run(command, stdout=subprocess.PIPE)
sys.stdout = sys.__stdout__

