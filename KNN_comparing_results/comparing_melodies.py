import os
import pickle
from sklearn.neighbors import NearestNeighbors
import utility_functions
import xlsxwriter


# Reading previously saved files
path = 'D:\\Studia\\praca-python\\nneighbors\\3_4-kneighbors'
# path = 'D:\\Studia\\praca-python\\nneighbors\\4_4-kneighbors'

with open(os.path.join(path, 'generated_melodies'), 'rb') as file:
    generated_melodies = pickle.load(file)

with open(os.path.join(path, 'generated_rhythms'), 'rb') as file:
    generated_rhythms = pickle.load(file)

with open(os.path.join(path, 'read_melodies'), 'rb') as file:
    read_melodies = pickle.load(file)

with open(os.path.join(path, 'read_rhythm'), 'rb') as file:
    read_rhythms = pickle.load(file)

with open(os.path.join(path, 'filenames'), 'rb') as file:
    filenames = pickle.load(file)


# Shortening and translating prepared dictations
generated_melodies = utility_functions.translate(generated_melodies, True)
generated_rhythms = utility_functions.translate(generated_rhythms, False)
read_melodies = utility_functions.translate(read_melodies, True)

# KNN neighbors
knn = NearestNeighbors(n_neighbors=5)
knn.fit(read_melodies)
distance_matrix, neighbours_index_matrix = knn.kneighbors(generated_melodies)

# Saving data to xlsx
workbook = xlsxwriter.Workbook(os.path.join(path, 'results.xlsx'))
worksheet_read_melodies = workbook.add_worksheet(name="read_melodies")
worksheet_generated_melodies = workbook.add_worksheet(name="generated_melodies")
worksheet_generated_rhythms = workbook.add_worksheet(name="generated_rhythms")
worksheet_distance_matrix = workbook.add_worksheet(name="distance")
worksheet_neighbors_index = workbook.add_worksheet(name="indices")

col = 0

for row, data in enumerate(filenames):  # filenames
    worksheet_read_melodies.write_string(row+1, col, data)
    worksheet_read_melodies.write_string(row + 1, col + 1, str(row))

# for row, data in enumerate(filenames):  # indices
#     worksheet_read_melodies.write_string(row+1, col+1, str(row))

for row, data in enumerate(read_melodies):  # read melodies
    worksheet_read_melodies.write_row(row+1, col+2, data)

for row, data in enumerate(generated_melodies):  # generated melodies
    worksheet_generated_melodies.write_row(row+1, col+2, data)

for row, data in enumerate(generated_rhythms):  # generated rhythm
    worksheet_generated_rhythms.write_row(row+1, col+2, data)

for row, data in enumerate(distance_matrix):  # distance matrix
    worksheet_distance_matrix.write_row(row+1, col+2, data)

for row, data in enumerate(neighbours_index_matrix):  # indices matrix
    worksheet_neighbors_index.write_row(row+1, col+2, data)

workbook.close()
