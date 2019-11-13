#!/usr/bin/env python
# coding: utf-8
# citations: 
# * https://www.kaggle.com/amarpreetsingh/stock-prediction-lstm-using-keras
# * https://docs.scipy.org/doc/numpy/reference/routines.array-manipulation.html
# * https://pythonprogramming.net/recurrent-neural-network-deep-learning-python-tensorflow-keras/
# * https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
# * https://towardsdatascience.com/recurrent-neural-networks-by-example-in-python-ffd204f99470
# * https://towardsdatascience.com/choosing-the-right-hyperparameters-for-a-simple-lstm-using-keras-f8e9ed76f046
# Library for manipulating, formatting, and cleaning the data
import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM,Dense,Dropout
import matplotlib.pyplot as plt

# Process data into 7 day look back slices
def processData(data,lb):
    X,Y = [],[]
    for i in range(len(data)-lb-1):
        X.append(data[i:(i+lb),0])
        Y.append(data[(i+lb),0])
    return np.array(X),np.array(Y)

def main():
    # Need to read data from Joseph's database
    print ("Current Company Code: " + str(sys.argv[1]))
    companyCode = str(sys.argv[1])

    data = pd.read_csv('./input/all_stocks_5yr.csv')
    closeData = data[data['Name']== companyCode].close
    closeData = closeData.values.reshape(closeData.shape[0], 1)
    scl = MinMaxScaler()
    closeData = scl.fit_transform(closeData)
    X,y = processData(closeData,7)
    X_train,X_test = X[:int(X.shape[0]*0.80)],X[int(X.shape[0]*0.80):]
    y_train,y_test = y[:int(y.shape[0]*0.80)],y[int(y.shape[0]*0.80):]

    # Build the model
    model = Sequential()
    model.add(LSTM(10,input_shape=(7,1)))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam',loss='mse')

    # Reshape data for (Sample,Timestep,Features) 
    X_train = X_train.reshape((X_train.shape[0],X_train.shape[1],1))
    X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))
    history = model.fit(X_train,y_train,epochs=200,validation_data=(X_test,y_test),shuffle=False)

    # Plot loss function
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    Xt = model.predict(X_test)
    plt.plot(scl.inverse_transform(y_test.reshape(-1,1)))
    plt.plot(scl.inverse_transform(Xt))
    act = []
    pred = []
    for i in range(250):
        Xt = model.predict(X_test[i].reshape(1,7,1))
        # print('predicted:{0}, actual:{1}'.format(scl.inverse_transform(Xt),scl.inverse_transform(y_test[i].reshape(-1,1))))
        pred.append(scl.inverse_transform(Xt))
        act.append(scl.inverse_transform(y_test[i].reshape(-1,1)))
    result_df = pd.DataFrame({'pred':list(np.reshape(pred, (-1))),'act':list(np.reshape(act, (-1)))})

    # Export model of company to modelBin
    try:
        os.mkdir('./modelBin/')
    except:
        pass
    try:
        os.mkdir('./modelBin/' + companyCode)
    except:
        pass
    model_json = model.to_json()
    with open('./modelBin/' + companyCode + '/model.json','w+') as json_file:
        json_file.write(model_json)
    model.save_weights('./modelBin/' + companyCode + '/model.h5')

if __name__ == '__main__':
    main()
