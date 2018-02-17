import csv
import datetime
import pickle
import socket
import sys

###

host = 'localhost'
port = 8002
matrix_dimension = int(sys.argv[1])
number_of_clients = int(sys.argv[2])
client_number = int(sys.argv[3])
matrix_a = list(csv.reader(open('a.csv'), quoting=csv.QUOTE_NONNUMERIC))
matrix_b = list(csv.reader(open('b.csv'), quoting=csv.QUOTE_NONNUMERIC))
matrix_c = list(csv.reader(open('c.csv'), quoting=csv.QUOTE_NONNUMERIC))
matrix_temp = []
matrix_d = []
counter = 0

height_start = client_number * (matrix_dimension // number_of_clients)
height_end = height_start + (matrix_dimension // number_of_clients)
width = matrix_dimension

print("%s:%s:%s" % (height_start, height_end, matrix_dimension))
start_time = datetime.datetime.now()
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
time_diff = datetime.datetime.now() - start_time
print("Execution time: %s" % time_diff)
