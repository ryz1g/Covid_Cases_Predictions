import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import model_from_json
import csv
from os import system

json_file = open('model_final.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model_final.h5")
f=open("case_time_series.csv")
lt=len(f.read().split("\n"))

def clear() :
    _=system("cls")

clear()

num=int(input("Enter Days for forecast:"))

daily_new=[]
days=range(1,lt+num-1)

with open("case_time_series.csv") as csvfile:
    reader=csv.reader(csvfile, delimiter=",")
    next(reader)
    for row in reader:
        daily_new.append(int(row[1]))

pred=[]
for i in range(num):
    pp=np.array(daily_new[-28:])
    #print(pp.shape)
    #print(pp)
    #print(pp[2])
    daily_new.append(int(loaded_model.predict(pp.reshape(1,28))))

f=open("case_time_series.csv")
st=f.read().split("\n")

print("From:"+st[len(st)-2].split(",")[0])
print(daily_new[lt-1:])
print("Cases predicted will be from one day after the above mentioned date\nCredibility of prediction will decrease after every predicted day")

plt.plot(days[:lt-2],daily_new[:lt-2])
plt.plot(days[lt-3:],daily_new[lt-3:])
plt.xlabel("Days since March 1")
plt.ylabel("Daily New Cases")
plt.title("Analysis")
plt.show()
