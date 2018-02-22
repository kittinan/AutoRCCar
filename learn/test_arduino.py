import serial
import pygame
import struct

s = serial.Serial('/dev/ttyACM1', 115200, timeout=1)


pygame.init()
pygame.display.set_mode((100, 100))
#pygame.display.set_mode()
while True:
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
