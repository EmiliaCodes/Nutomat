import engine
import os
import pickle


# Using engine python script from Nutomat application - you need to modify the code by changing
# the line in generate() function --> "while actual_length < desired_length:" to "for i in range(0, 16):"
my_engine = engine.Engine()
path_save = 'D:\\Studia\\praca-python\\nneighbors\\3_4-kneighbors\\generated_dictations'
# path_save = 'D:\\Studia\\praca-python\\nneighbors\\4_4-kneighbors\\generated_dictations'
number_of_bars = 20.0
key_signature = "C-dur"
tempo = "szybkie"
write_midi = False
write_empty = False
hints = 0
time_signature = "3/4"  # 4/4
temperature = 1.2  # 0.5

generated_dictations_pitch = []
generated_dictations_rhythm = []

# Generate 100 dictations
for i in range(0, 100):
    pitch_final_prediction, rhythm_final_prediction = my_engine.generate(temperature, number_of_bars,
                                                                         time_signature)
    my_engine.save_file(pitch_final_prediction, rhythm_final_prediction, path_save, key_signature,
                        tempo, write_midi, write_empty, hints, time_signature)
    print(i)  # show the progress
    generated_dictations_pitch.append(pitch_final_prediction)
    generated_dictations_rhythm.append(rhythm_final_prediction)

# Save the data
with open(os.path.join(path_save, 'generated_melodies'), 'wb') as file:
    pickle.dump(generated_dictations_pitch, file)

with open(os.path.join(path_save, 'generated_rhythms'), 'wb') as file:
    pickle.dump(generated_dictations_rhythm, file)