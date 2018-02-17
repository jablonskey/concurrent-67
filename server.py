import csv
import datetime
import pickle
import random
import socket
import sys

import numpy

###
host = 'localhost'
port = 8002
matrix_dimension = int(sys.argv[1])


###

def export_matrix(matrix, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)


def random_box_matrix(dimension, max_number=5):
    return [[random.randint(0, max_number) for j in range(dimension)] for i in range(dimension)]


matrix_a = random_box_matrix(matrix_dimension)
export_matrix(matrix_a, 'a.csv')
matrix_b = random_box_matrix(matrix_dimension)
export_matrix(matrix_b, 'b.csv')
matrix_c = random_box_matrix(matrix_dimension)
export_matrix(matrix_c, 'c.csv')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

received_parts = 0
transfer_errors = 0
result_matrix = [[None for _ in range(matrix_dimension)] for _ in range(matrix_dimension)]

start_time = 0
while received_parts < matrix_dimension:
    try:
        conn, addr = s.accept()
        tm = conn.recv(32768)
        if (start_time is 0):
            start_time = datetime.datetime.now()
        part = pickle.loads(tm)

    except pickle.UnpicklingError:
        print('ERR %s in [%s][0:%s]' % (sys.exc_info(), part[1], part[2]))
        transfer_errors += 1

    finally:
        conn.close()
        # print(part)
        result_matrix[part[1]][0:part[2] + 1] = part[3]

        received_parts += 1
        print('id :: %s :: [%s][0:%s] :: total: %s' % (part[0], part[1], part[2], received_parts))

time_diff = datetime.datetime.now() - start_time
if transfer_errors is not 0:
    print("Errors: ", transfer_errors)
print("Execution time: %s" % time_diff)

correct_matrix_temp = numpy.matmul(matrix_a, matrix_b).tolist()
correct_matrix_d = numpy.matmul(correct_matrix_temp, matrix_c).tolist()
export_matrix(correct_matrix_d, 'correct_d.csv')
export_matrix(result_matrix, 'received_matrix_d.csv')

print('Correct result: ', numpy.array_equal(correct_matrix_d, result_matrix))
