# Covid_Cases_Predictions

A program to give forecast of expected number of Covid cases on the basis of data from last 28 days.

Files included:-

1)case_time_series.csv - Time series data of Covid cases from 1st March 2020 in India updated every day.  (https://api.covid19india.org/csv/latest/case_time_series.csv)

2)model.py - Python script to train the model on the basis of previous data. Uses Keras.

3)predict.py - Asks for number of days the forecast is needed and prints the forecasts along with drawing graphs.

4)model_fianl.json - Model specifications in json format for easier loading

5)model_final.h5 - Saved weights
