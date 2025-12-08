import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "./data_h15_test.csv"

df = pd.read_csv(file_path, index_col=False)

times = df["time"].to_numpy()
speed = df["Speed"].to_numpy()
servo = df["Servo"].to_numpy()

print(speed)
plt.plot(times, speed)
plt.plot(times, servo)
plt.show()
