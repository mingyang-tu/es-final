import socket
import json
import numpy as np
import matplotlib.pyplot as plt


class LinearRegression:
    def __init__(self, x, y):
        if len(x.shape) == 1:
            x = x.reshape(-1, 1)
        if len(y.shape) == 1:
            y = y.reshape(-1, 1)
        self.num_sample = x.shape[0]
        self.dim = x.shape[1] + 1
        self.x = np.concatenate([np.ones((self.num_sample, 1)), x], axis=1)
        self.y = y

        self.weight = np.dot(np.linalg.pinv(self.x), self.y)

    def predict(self, data):
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        data = np.concatenate([np.ones((self.num_sample, 1)), data], axis=1)
        return np.dot(data, self.weight)


section = 2

NUM_OF_SAMPLES = 1000

if section == 1:
    HOST = "192.168.50.70"
    PORT = 9876

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.settimeout(1)
    print(f'Bind {HOST}:{PORT}')

    gyro = []
    acce_x = []
    acce_z = []
    n = 0

    while n < NUM_OF_SAMPLES:
        try:
            data, _ = s.recvfrom(1024)
            data = json.loads(data)
            print("Data: ", data, end="\r")
            gyro.append(data["gyro"])
            acce_x.append(data["acce_x"])
            acce_z.append(data["acce_z"])
            n += 1
        except socket.timeout:
            print("Not received...", end="\r")
        except:
            pass

    np.save("./data/gyro.npy", np.array(gyro))
    np.save("./data/acce_x.npy", np.array(acce_x))
    np.save("./data/acce_z.npy", np.array(acce_z))

elif section == 2:
    gyro = np.load("./data/gyro.npy") * (-0.025 / 1000)
    acce_x = np.load("./data/acce_x.npy")
    acce_z = np.load("./data/acce_z.npy")
    n = gyro.shape[0]
    datas = dict()

    # accelerometer
    angle_a = np.arctan2(acce_x, acce_z) / np.pi * 180
    angle_a -= angle_a[0]
    datas["accelerometer"] = angle_a

    # gyroscope
    angle_g = np.zeros(n)
    accumulate = 0
    for i in range(n):
        accumulate += gyro[i]
        angle_g[i] = accumulate
    datas["gyroscope (accumulated)"] = angle_g

    # complementary filter
    complementary = np.zeros(n)
    accumulate = 0
    for i in range(n):
        accumulate = 0.98 * (accumulate + gyro[i]) + 0.02 * angle_a[i]
        complementary[i] = accumulate
    datas["complementary filter"] = complementary

    idxs = np.arange(n)
    colors = ["tab:blue", "tab:orange", "tab:green"]

    for i, (label, data) in enumerate(datas.items()):
        model = LinearRegression(idxs, data)
        predict = model.predict(idxs)
        weight = model.weight

        plt.plot(idxs, data, color=colors[i], label=label)
        plt.plot(
            idxs, predict,
            linestyle='--',
            color=colors[i],
            label=f"offset={weight[0, 0]:.3f}, slope={weight[1, 0]:.3e}"
        )

    plt.ylabel("degree")
    plt.legend()
    plt.show()
