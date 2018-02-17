import csv
import socket
import pickle
import sys
import numpy

###
import time

host = 'localhost'
port = 8002
matrix_dimension = int(sys.argv[1])
number_of_clients = int(sys.argv[2])
# matrix_dimension = 128
# number_of_clients = 1

matrix_a = list(csv.reader(open('a.csv'), quoting=csv.QUOTE_NONNUMERIC));
matrix_b = list(csv.reader(open('b.csv'), quoting=csv.QUOTE_NONNUMERIC));
matrix_c = list(csv.reader(open('c.csv'), quoting=csv.QUOTE_NONNUMERIC));

client_number = int(sys.argv[3])
# client_number = 0

height_start = client_number * (matrix_dimension // number_of_clients)
height_end = height_start + (matrix_dimension // number_of_clients)
width = matrix_dimension

matrix_temp = [];
matrix_d = [];
counter = 0

print("%s:%s:%s" % (height_start, height_end, matrix_dimension))

for i in range(height_start, height_end):
    matrix_temp.append([])
    for j in range(0, width):
        matrix_temp[counter].append(0)
        for k in range(0, width):
            matrix_temp[counter][j] += matrix_a[i][k] * matrix_b[k][j]

    matrix_d.append([])
    for j in range(0, width):
        matrix_d[counter].append(0)
        for k in range(0, width):
            matrix_d[counter][j] += matrix_temp[counter][k] * matrix_c[k][j]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(pickle.dumps((client_number, i, j, matrix_d[counter][0:j + 1]), protocol=pickle.HIGHEST_PROTOCOL))
    s.close()
    counter += 1
