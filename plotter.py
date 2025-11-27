import matplotlib.pyplot as plt
import pandas as pd


def extract_gyro(file):
    df = pd.read_csv(file, delimiter=";", names=["AngspeedZ", "setpoint", "speederr", "intErr", "cmd", "time"], index_col=False)
    return df["time"].to_numpy(), df["AngspeedZ"].to_numpy()

files_to_read = ["data_Helice20.csv", "data_Helice25.csv", "data_Helice30.csv", "data_Helice40.csv", "data_Helice50.csv"]
#for file in files_to_read:
#    times, gyro = extract_gyro(file)
#    plt.plot(times, gyro, label={file})

#plt.legend()
#plt.show()

df = pd.read_csv("data.csv", delimiter=";", names=["AngspeedZ", "setpoint", "speederr", "intErr", "cmd", "time"], index_col=False)

print(df["AngspeedZ"].to_numpy())
print(df["setpoint"].to_numpy())
print(df["speederr"].to_numpy())
print(df["intErr"].to_numpy())
print(df["cmd"].to_numpy())
print(df["time"].to_numpy())

print(df.columns)

figure, axis = plt.subplots(2, 1)

axis[0].plot(df["time"].to_numpy(), df["intErr"].to_numpy(), label="intErr")
axis[0].plot(df["time"].to_numpy(), df["cmd"].to_numpy(), label="cmd")
axis[0].legend()


axis[1].plot(df["time"].to_numpy(), df["AngspeedZ"].to_numpy(), label="AngspeedZ")
axis[1].plot(df["time"].to_numpy(), df["speederr"].to_numpy(), label="speederr")
axis[1].plot(df["time"].to_numpy(), df["setpoint"].to_numpy(), label="setpoint")
axis[1].legend()

plt.show()