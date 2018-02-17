import csv
import socket
import pickle
import time
import sys
import numpy

###
host = 'localhost'
port = 8002
matrix_dimension = int(sys.argv[1])
# matrix_dimension = int(128)
###
matrix_a = list(csv.reader(open('a.csv'), quoting=csv.QUOTE_NONNUMERIC));
matrix_b = list(csv.reader(open('b.csv'), quoting=csv.QUOTE_NONNUMERIC));
matrix_c = list(csv.reader(open('c.csv'), quoting=csv.QUOTE_NONNUMERIC));

correct_matrix_temp = numpy.matmul(matrix_a, matrix_b)
correct_matrix_d = numpy.matmul(correct_matrix_temp, matrix_c)

with open('correct_matrix_d.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(correct_matrix_d)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

received_parts = 0
result = [[None for _ in range(matrix_dimension)] for _ in range(matrix_dimension)]

start_time = time.time()
while received_parts < matrix_dimension:
    conn, addr = s.accept()
    tm = conn.recv(500000)
    part = pickle.loads(tm)

    conn.close()
    # print(part)
    result[part[1]][0:part[2]] = part[3]

    received_parts += 1
    print('id :: %s :: [%s][0:%s] :: total: %s' % (part[0], part[1], part[2], received_parts))


print("Execution time: {}s".format(time.localtime(time.time() - start_time).tm_sec))

print('Correct result: ', numpy.array_equal(correct_matrix_d, result))

with open('received_matrix_d.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(result)
