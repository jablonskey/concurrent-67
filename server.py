import csv
import socket
import pickle
import time
import sys

###
host = 'localhost'
port = 8002
matrix_dimension = int(sys.argv[1])
###

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

received_parts = 0
result = [[None for _ in range(matrix_dimension)] for _ in range(matrix_dimension)]

start_time = time.time()
while received_parts < matrix_dimension:
    conn, addr = s.accept()
    print('Client connected: ', addr)
    tm = conn.recv(8192)
    part = pickle.loads(tm)
    conn.close()
    # print(part)
    result[part[1]][1:part[2]] = part[3]

    received_parts += 1
    print(received_parts)

print("Execution time: {}s".format(time.localtime(time.time() - start_time).tm_sec))

writer = csv.writer(open('e.csv', 'w'))
writer.writerows(result)
