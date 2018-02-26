import serial
import pygame
import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import zlib


s = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


pygame.init()
pygame.display.set_mode((100, 100))


HOST=''
PORT=8484

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

#pygame.display.set_mode()

count_frame = 0
saved_frame = 0

while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    #frame = frame_data
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.imwrite('data/images/frame_{:>05}.jpg'.format(count_frame), image)
    cv2.waitKey(1)

    count_frame+= 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                print("Forward Right")
                s.write(struct.pack('>B', 6))
            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                print("Forward Left")
                s.write(struct.pack('>B', 7))

            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                print("Reverse Right")
                s.write(struct.pack('>B', 8))

            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                print("Reverse Left")
                s.write(struct.pack('>B', 9))
            elif key_input[pygame.K_LEFT]:
                print("left")
                s.write(struct.pack('>B', 4))
            elif key_input[pygame.K_RIGHT]:
                print("right")
                s.write(struct.pack('>B', 3))
            elif key_input[pygame.K_UP]:
                print("up")
                s.write(struct.pack('>B', 1))
            elif key_input[pygame.K_DOWN]:
                print("down")
                s.write(struct.pack('>B', 2))
            elif key_input[pygame.K_DELETE]:
                print("reset")
                s.write(struct.pack('>B', 0))
