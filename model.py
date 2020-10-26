import csv
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam

active_cases=[]
daily_new=[]
days=[]
c=0

def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.show()

preeev=0
with open("case_time_series.csv") as csvfile:
    reader=csv.reader(csvfile, delimiter=",")
    next(reader)
    for row in reader:
        c=c+1
        if c==1 :
            active_cases.append(3+int(row[1])-int(row[3]))
        else :
            active_cases.append(active_cases[c-2]+int(row[1])-int(row[3]))
        if preeev==0 :
            daily_new.append(int(row[1]))
            preeev=int(row[1])
        else :
            daily_new.append(int(row[1])-preeev)
            preeev=int(row[1])
        days.append(c)

temp_1=[]
l=0
temp_daily=[]

#hyperparameters for training
window_size=28
num_epochs=3000
bat=300
op=Adam(lr=0.00000001)
lol="mae"
verb=2

for i in active_cases:
    if l+window_size>=len(active_cases):
        break
    temp=active_cases[l:l+window_size+1]
    temp_1.append(temp)
    temp=daily_new[l:l+window_size+1]
    temp_daily.append(temp)
    l=l+1

xs_daily,ys_daily=([],[])
for i in temp_daily:
    xs_daily.append(i[:-1])
    ys_daily.append(i[-1:])

xs_daily=np.array(xs_daily)
ys_daily=np.array(ys_daily)

model= tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(2000, input_shape=[window_size], activation="relu"))
model.add(tf.keras.layers.Dense(1500, activation="relu"))
model.add(tf.keras.layers.Dense(1000, activation="relu"))
model.add(tf.keras.layers.Dense(500, activation="relu"))
model.add(tf.keras.layers.Dense(100, activation="relu"))
model.add(tf.keras.layers.Dense(50, activation="relu"))
model.add(tf.keras.layers.Dense(15, activation="relu"))
model.add(tf.keras.layers.Dense(1))
model.load_weights("model_final.h5")
model.compile(optimizer=op, loss=lol, metrics=['accuracy'])
history=model.fit(xs_daily,ys_daily,verbose=verb,epochs=num_epochs,batch_size=bat)

model.summary()

ti=input("save weights?(Y/N)")
if ti=="Y" :
    model_json=model.to_json()
    with open("model_final.json", "w") as json_file :
        json_file.write(model_json)
    model.save_weights("model_final.h5")

pred_fit=[]
for i in xs_daily:
    pred_fit.append(model.predict(i.reshape((1,window_size))))
pred_fit=np.array(pred_fit).reshape(len(xs_daily))

plt.plot(range(1,len(ys_daily)+1),ys_daily)
plt.plot(range(1,len(pred_fit)+1),pred_fit)
plt.xlabel("Days")
plt.ylabel("Daily New Cases")
plt.title("Analysis")
plt.show()

plot_graphs(history, "loss")
