import socket
import json
import numpy as np
import matplotlib.pyplot as plt

section = 2

NUM_OF_SAMPLES = 200
MAGNITUDE = 1070

if section == 1:
    HOST = "192.168.50.70"
    PORT = 9876

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.settimeout(1)
    print(f'Bind {HOST}:{PORT}')

    gyro = []
    acce = []
    n = 0

    while n < NUM_OF_SAMPLES:
        try:
            data, _ = s.recvfrom(1024)
            data = json.loads(data)
            print("Data: ", data, end="\r")
            gyro.append(data["gyro"])
            acce.append(data["acce_x"])
            n += 1
        except socket.timeout:
            print("Not received...", end="\r")
        except:
            pass

    np.save("./data/gyro.npy", np.array(gyro))
    np.save("./data/acce.npy", np.array(acce))

elif section == 2:
    gyro = np.load("./data/gyro.npy") * 0.005 / 100
    acce = np.load("./data/acce.npy")

    n = gyro.shape[0]

    angle_a = np.arcsin(acce / MAGNITUDE) / np.pi * 180
    angle_a -= angle_a[0]

    angle_g = np.zeros(n)
    accumulate = 0
    for i in range(n):
        accumulate -= gyro[i]
        angle_g[i] = accumulate

    complementary = np.zeros(n)
    accumulate = 0
    for i in range(n):
        accumulate = 0.98 * (accumulate - gyro[i]) + 0.02 * angle_a[i]
        complementary[i] = accumulate

    idxs = np.arange(n)
    plt.plot(idxs, angle_a)
    plt.plot(idxs, angle_g)
    plt.plot(idxs, complementary)
    plt.ylabel("degree")
    plt.legend(["accelerometer", "gyroscope (accumulated)", "complementary filter"])
    plt.show()
