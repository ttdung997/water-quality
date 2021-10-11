import sklearn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain, combinations
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import datetime
import pickle
import sys
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.layers import Dropout


from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import GRU
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras import layers
from tensorflow.keras import backend as K

from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import sequence
from scipy import interp
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from sklearn.linear_model import LinearRegression
from matplotlib.dates import (YEARLY, DateFormatter,
    rrulewrapper, RRuleLocator, drange)
#load excel dataframe

TRAINING_FLAG = 0

class FuzzyLayer(layers.Layer):
    def __init__(self, initializer="he_normal", **kwargs):
        super(FuzzyLayer, self).__init__(**kwargs)
        self.initializer = tf.keras.initializers.get(initializer)

    def build(self, input_shape):
        output_dim = input_shape[-1]
        self.output_dim = output_dim
        self.a1 = self.add_weight(
            shape=(1, output_dim),
            initializer=self.initializer,
            name="a1",
            trainable=True,
        )
        self.b1 = self.add_weight(
            shape=(1 , output_dim),
            initializer=self.initializer,
            name="b1",
            trainable=True,
        )
        self.a2 = self.add_weight(
            shape=(1, output_dim),
            initializer=self.initializer,
            name="a2",
            trainable=True,
        )
        self.b2 = self.add_weight(
            shape=(1 , output_dim),
            initializer=self.initializer,
            name="b2",
            trainable=True,
        )
        self.a3 = self.add_weight(
            shape=(1, output_dim),
            initializer=self.initializer,
            name="a3",
            trainable=True,
        )
        self.b3 = self.add_weight(
            shape=(1 , output_dim),
            initializer=self.initializer,
            name="b3",
            trainable=True,
        )
        self.a1 = K.repeat_elements(K.expand_dims(0.0, axis = -1), self.output_dim, -1)
        self.a2 = K.repeat_elements(K.expand_dims(0.0, axis = -1), self.output_dim, -1)
        self.a3 = K.repeat_elements(K.expand_dims(0.0, axis = -1), self.output_dim, -1)

        self.b1 = K.repeat_elements(K.expand_dims(10.0, axis = -1), self.output_dim, -1)
        self.b2 = K.repeat_elements(K.expand_dims(10.0, axis = -1), self.output_dim, -1)
        self.b3 = K.repeat_elements(K.expand_dims(10.0, axis = -1), self.output_dim, -1)
    
    # @tf.function
    def call(self, inputs):
        # inputs -= tf.reduce_mean(inputs, axis=-1, keepdims=True)
        x = inputs
        # x1 = 1/(1+tf.math.exp(-self.a1*(x+self.b1)))
        # x2 = tf.math.exp(-tf.math.pow(x-self.b2,2)/(2*tf.math.pow(self.a2,2)))
        # x3 = 1/(1-tf.math.exp(self.a3*(x+self.b3)))
        # print(x)
        # print(self.a1)
        
        low = [0.0 for x in range(0,10)]
        low = [low for x in range(0,10)]
        low = tf.convert_to_tensor(low,dtype = "float")
        # print(x1)
        low = tf.reshape(low,(1,10,10))

        x1 = (x- self.a1)/(self.b1 - self.a1)
        x2 = (x- self.b1)/(self.a1 - self.b1)
        x3 = (x- self.b3)/(2*self.a3 - self.b3)
        # return x1

        high = [10.0 for x in range(0,10)]
        high = [high for x in range(0,10)]
        high = tf.convert_to_tensor(high,dtype = "float")
        # print(x1)
        high = tf.reshape(high,(1,10,10))

        
        return tf.concat([x1,x2,x3],-1)

        if tf.math.less_equal(x,self.a1):
            x1 = low
        elif tf.math.greater(x,self.a1)  and tf.math.greater(self.b1,x):
            x1 = (x- self.a1)/(self.b1 - self.a1)
        else:
            x1 = high
          
        if tf.math.less_equal(x,self.a2):
            x2 = low
        elif tf.math.greater(x,self.a2)  and tf.math.greater(self.b2,x):
            x2 = (x- self.a2)/(self.b2 - self.a2)
        else:
            x2 = high

        if tf.math.less_equal(x,self.a3) or tf.math.less_equal(2*self.a3,x) :
            x3 = low
        elif tf.math.greater(x,self.a3)  and tf.math.greater(self.b3,x):
            x3 = (x- self.a3)/(self.b3 - self.a3)
        elif tf.math.greater(x,self.b3)  and tf.math.greater(2*self.a3,x):
            x3 = (x- self.b3)/(2*self.a3 - self.b3)
        elif x == 2*self.a3:
            x3 = high
        else:
            x3 = low

        # x1 = K.repeat_elements(K.expand_dims(0.0, axis = -1), self.output_dim, -1)

        # x2 = K.repeat_elements(K.expand_dims(0.0, axis = -1), self.output_dim, -1)

        # x3 = K.repeat_elements(K.expand_dims(0.0, axis = -1), self.output_dim, -1)

        # x1 = (x- self.a1)/(self.b1 - self.a1)

        # print(x1.shape)
        # print(x2.shape)
        # print(x3.shape)

        # print("WTD")
        # print(x)
        # print(x[0][0][0])
        # quit()
        # print(x1)
        # print(tf.concat([x1,x2,x3],-1))
        # print(tf.concat([x1,x2,x3],-1).shape)
        # quit()
        # xc = inputs*aligned_a
        # print(tf.concat([x1,x2,x3],-1).shape)
        return tf.concat([x1,x2,x3],-1)
        # return x1

def build_anfis_model(inputs, output_size, neurons, activ_func="linear",
    dropout=0.25, loss="mae", optimizer="adam"):
    model = Sequential()
    model.add(FuzzyLayer(input_shape=(10, 7)))

    model.add(SimpleRNN(neurons, input_shape=(inputs.shape[1], inputs.shape[2])))
    # model.add(DefuzzyLayer(1))
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))
    model.compile(loss=loss, optimizer=optimizer)
    return model


dataCol = ['Name (E)' ,'YY/MM','NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
 'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
  'Hydrogen ion conc.','DO (㎎/L)', 'TSI(Chl-a)']

dataCol = ['Name (E)' ,'YY/MM','NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
 'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
  'Hydrogen ion conc.','DO (㎎/L)','BOD(㎎/L)',"I(pH)",]

dataCol = ['Name (E)' ,'YY/MM','NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
 'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
  'Hydrogen ion conc.','DO (㎎/L)','BOD(㎎/L)',"I(pH)","K-CWQI","Temp.(℃)", 'TSI(Chl-a)']



dataCol = ['Name (E)' ,'YY/MM','NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
 'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)',  'TSI(Chl-a)']


# dataCol = ['Name (E)' ,'YY/MM','Dissolved Total N(㎎/L)', 'NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'Dissolved Total P(㎎/L)','Conductivity(µS/㎝)','TSI(Chl-a)']

# norm_cols = ['Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
  # 'Hydrogen ion conc.','DO (㎎/L)','BOD(㎎/L)',"I(pH)", 'TSI(Chl-a)']


# norm_cols = ['NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
#  'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
#   'Hydrogen ion conc.','DO (㎎/L)','BOD(㎎/L)',"Temp.(℃)", 'TSI(Chl-a)']

norm_cols = ['NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
 'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)', 'TSI(Chl-a)']


MasterDataframe = pd.read_excel('predata2.xls')
MasterDataframe.rename(columns=MasterDataframe.iloc[0])
#Get all subset of the column
ColumnList = list(MasterDataframe)
# print(ColumnList)
# quit()


# print(MasterDataframe.head())

MasterDataframe2 = pd.read_excel('Data.xlsx')
MasterDataframe2.rename(columns=MasterDataframe2.iloc[0])
#Get all subset of the column
# ColumnList = list(MasterDataframe)


df1 = MasterDataframe[dataCol]
df2 = MasterDataframe2[dataCol]

df = pd.concat([df1,df2])



# print(df)

# quit()
# print(correlation)
# correlation = correlation.values

### Calculate correlation

# # print(correlation[0][0])
# print(len(dataCol))
# for i in range(0,len(correlation)-1):
#   for j in range(0,len(correlation)-1):
#       if i==j:
#           continue
#       if correlation[i][j] > 0:
#           print(dataCol[i] + "<--->" + dataCol [j] +" ||| correlation: "+str(correlation[i][j]))

# quit()


# print(df.head())
# print(df.describe())

# print(df.isnull().sum())


for col in dataCol:
    print(col)
    try:
        median = df[col].median()
        # print(median)
        # print("_____________________+")
        df[col].fillna(median, inplace=True)
    except:
        continue
        # print(col)
        # print("it here")
        # df[col].fillna("Mesotrophic", inplace=True)



# df =df[norm_cols]
# chla = df['TSI(Chl-a)'].values
# label =[]
# for i in range(0,len(chla)):
#     # print(df['TSI(Chl-a)'][i])
#     if chla[i] > 60:
#         label.append("on")
#     else:
#         label.append("off")

# df["final"] = label
# df.to_csv("c45.csv")

# quit()

window_len = 10
print(df.head())

myDf = df[dataCol]
myDf = myDf.sort_values(by='YY/MM')

dictrictArr = (myDf['Name (E)'].unique())

training_input = np.empty((1,window_len,6))
training_output = np.empty((1,))
test_input = np.empty((1,window_len,6))
test_output = np.empty((1,))


# print(training_input)
# print(test_input)
# quit()

# norm_cols = ['Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
# 'Hydrogen ion conc.','DO (㎎/L)','BOD(㎎/L)',"I(pH)","K-CWQI","Temp.(℃)", 'TSI(Chl-a)']

count = 0

dictrictMSE = []
dictrictName =  []

finalArr = []
finalArr2 = []

for dictrict in dictrictArr:
    try:
        print(dictrict)
        count = count + 1
        small_data = df[df['Name (E)']==dictrict]
        small_data = small_data.drop('Name (E)', 1)
        print(len(small_data))
        timeframe = small_data['YY/MM'].values
        # small_data = small_data.drop('YY/MM', 1)
        # small_data = small_data.values
        # print(small_data)
        # print(small_data.shape)
        # np.savetxt(str(dictrict)+".txt",small_data,delimiter=' ' ,fmt='%1.4e') 

        # training_set = training_set.drop('YY/MM', 1)
        # print(list(small_data))
        # small_data.to_csv("fdata/"+dictrict+".csv",index=False)
        # quit()
        # continue
        split_date = "2018/09"
        training_set, test_set = small_data[small_data['YY/MM']<split_date], small_data[small_data['YY/MM']>=split_date]

        training_set = training_set.drop('YY/MM', 1)
        test_set = test_set.drop('YY/MM', 1)
        training_set=training_set.astype('float')

        test_set=test_set.astype('float')

        # print(training_set)
        # print(test_set)

        LSTM_training_inputs = []
        for i in range(len(training_set)-window_len):
            temp_set = training_set[i:(i+window_len)].copy()
            for col in norm_cols:
                temp_set.loc[:, col] = temp_set[col]
                # print(temp_set)
                # LSTM_training_inputs = []
            LSTM_training_inputs.append(temp_set)


        LSTM_test_inputs = []
        for i in range(len(test_set)-window_len):
            temp_set = test_set[i:(i+window_len)].copy()
            for col in norm_cols:
                temp_set.loc[:, col] = temp_set[col]
        # print(temp_set)
            LSTM_test_inputs.append(temp_set)
        
        LSTM_test_outputs = test_set['TSI(Chl-a)'][window_len:].values

        LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
        LSTM_training_inputs = np.array(LSTM_training_inputs)

        LSTM_test_inputs = [np.array(LSTM_test_inputs) for LSTM_test_inputs in LSTM_test_inputs]
        LSTM_test_inputs = np.array(LSTM_test_inputs)

        # print(LSTM_last_input.shape)
        # LSTM_last_input.to_csv("lastdata.csv")
        # LSTM_last_input = LSTM_test_inputs[-1]
        # LSTM_last_input.shape = (1,10,4)

        np.random.seed(202)
        # print(training_set['TSI(Chl-a)'][window_len:].values)
        # print("______________________")

        LSTM_training_outputs_raw = training_set['TSI(Chl-a)'][window_len:].values
        # print(LSTM_training_outputs_raw)
        LSTM_training_outputs = []
        for line in LSTM_training_outputs_raw:
            if line < 10:
                LSTM_training_outputs.append([1,0])
            elif line > 70:
                LSTM_training_outputs.append([0,1])
            else:
                temp = float(line-10)/70
                LSTM_training_outputs.append([1-temp,temp])

        # print("213123")
        # print(LSTM_training_inputs.shape)
        # print(LSTM_training_outputs.shape)
        # # print(training_input)
        # print(LSTM_training_inputs)
        # print(LSTM_training_outputs)
        dataInput = []
        for i in range(0, len(LSTM_training_inputs)):
            tem = list(LSTM_training_inputs[i][0])
            # print(tem)
            tem.append(LSTM_training_outputs[i])
            # print(LSTM_training_outputs[i])
            dataInput.append(tem)

        # print(dataInput)
 #        mydf = pd.DataFrame(dataInput,columns =['NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
 # 'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
 #  'Hydrogen ion conc.','DO (㎎/L)', 'TSI(Chl-a)','Predict'])

        # corr = mydf.corr()
        # corr.to_csv("cor/"+dictrict+".csv")
        # print(len(LSTM_test_inputs))
            
        # print(len(LSTM_test_outputs))
        # print("________________")
        # quit()
        if count > 1:
            training_input  = np.concatenate((training_input, LSTM_training_inputs), axis=0) 
            training_output = np.concatenate((training_output, LSTM_training_outputs), axis=0) 
            test_input = np.concatenate((test_input, LSTM_test_inputs), axis=0) 
            test_output = np.concatenate((test_output, LSTM_test_outputs), axis=0) 
        else:
            training_input = LSTM_training_inputs 
            training_output = LSTM_training_outputs 
            test_input = LSTM_test_inputs 
            test_output = LSTM_test_outputs 
        # my_model = ""
        # my_model = build_LSTM_model(LSTM_training_inputs, output_size=1, neurons = 100)
        # my_model.fit(LSTM_training_inputs, LSTM_training_outputs, 
        #   epochs=30, batch_size=1, verbose=1, shuffle=True)
        # predict =  my_model.predict(LSTM_test_inputs)

        # print(len(predict))

        # dates = [1,2,3,4,5,6,7,8]
        # # fig, ax1 = plt.subplots(1,1)
        # # print(LSTM_test_inputs)
        # # print("***************************************")
        # # print(predict)
        # # print(test_set['TSI(Chl-a)'][window_len-1:].values)
        # # print("____________________________________________________")
        # # print(LSTM_test_outputs)
        # predict_based = test_set['TSI(Chl-a)'][window_len-1:].values

        # final_predict = []
        # final_predict.append(predict_based[1])

        # loop = 0
        # check = 0
        # for i in range(1, len(predict_based)):
        #   if predict_based[i] == predict_based[i-1]:
        #       loop = loop +1
        #       if loop > 1:
        #           check = 1
        #           continue
        # if check == 1:
        #   continue
        # for i in range(1, len(predict)):
        #   temp = (1 + (predict[i]-predict[i-1])/predict[i-1])*predict_based[i-1]
        #   final_predict.append(temp)
        # print(final_predict)
        # mseValue = np.mean(np.abs((final_predict) - test_set['TSI(Chl-a)'][window_len:].values))/max(final_predict)
        
        # fig, ax1 = plt.subplots(1,1,figsize=(20,10))
        # ax1.plot(timeframe[:len(test_set['TSI(Chl-a)'][window_len:].values,)],test_set['TSI(Chl-a)'][window_len:].values, label='Actual')
        # ax1.plot(timeframe[:len(final_predict)],final_predict, label='Predicted')
        # ax1.annotate('MAE: %.4f'%mseValue, 
        #   xy=(0.75, 0.9),  xycoords='axes fraction',
        #   xytext=(0.75, 0.9), textcoords='axes fraction')

        # ax1.set_title("Dự đoán nổng độ tảo tại trạm "+dictrict,fontsize=13)
        # ax1.legend()
        # fig.autofmt_xdate()
        # ax1.set_ylim(bottom=0)
        # ax1.set_ylim(top=100)
        # # ax1.set_ylabel('gía cổ phiếu (VND)',fontsize=12)
        # # ax1.xaxis.set_major_locator(loc)
        # # ax1.xaxis.set_major_formatter(formatter)
        # # ax1.xaxis.set_tick_params(rotation=10, labelsize=10)
        # # ax1.set_ylim(bottom=0)
        # # ax1.set_ylim(top=100)
        # # plt.show()

        # dictrictName.append(dictrict)
        # dictrictMSE.append(mseValue)
        # finalArr.append(final_predict[-2:])
        # finalArr2.append( test_set['TSI(Chl-a)'][window_len:].values[-2:])

        # plt.savefig("rnn-tiny/"+ dictrict +'.png', dpi=100)
    except:
        continue
# y_pred = []
# print("final predict")
# for i in range(0, len(dictrictName)):
#   if finalArr[i][0] > 60 or finalArr[i][1] >60:
#       y_pred.append(1)
#   else:
#       y_pred.append(0)
#       # grade = "Eutrophy"
#       # if finalArr[i][0] > 70 or finalArr[i][1] >70:
#       #   grade = "Hypereutrophy"
#       # if finalArr[i][0] > 80 or finalArr[i][1] >80:
#       #   grade = "Algae bloom"
#       # print("tram "+ dictrictName[i]+ " co kha nang no hoa")
#       # print("Grade:" + grade) 

# y_true  = []
# print("final predict")
# for i in range(0, len(dictrictName)):
#   if finalArr2[i][0] > 60 or finalArr2[i][1] >60:
#       y_true.append(1)
#   else:
#       y_true.append(0)
#       # grade = "Eutrophy"
#       # if finalArr2[i][0] > 70 or finalArr2[i][1] >70:
#       #   grade = "Hypereutrophy"
#       # if finalArr2[i][0] > 80 or finalArr2[i][1] >80:
#       #   grade = "Algae bloom"
#       # print("tram "+ dictrictName[i]+ " co kha nang no hoa")
#       # print("Grade:" + grade) 

# print(y_true)
# print(len(y_true))
# print(y_pred)
# print(len(y_pred))

# from sklearn.metrics import classification_report
# print(classification_report(y_true, y_pred))
# quit()
# for i in range(0, len(dictrictName)):
#   print(dictrictName[i] + "||" + str(dictrictMSE[i]) + "|||")

# df = pd.DataFrame(list(zip(dictrictName, dictrictMSE)), 
#                columns =['Name', 'val']) 
# df.to_csv("tiny.csv")

# quit()
# print(len(training_input))
# print(len(training_output))
# mytestpd = pd.DataFrame(list(zip(training_input, training_output)), 
#                columns =['NH3-N(㎎/L)', 'NO3-N(㎎/L)', 'PO4-P(㎎/L)',
#            'T-N(㎎/L)','T-P(㎎/L)', 'Dissolved Total N(㎎/L)','Dissolved Total P(㎎/L)',
#             'Hydrogen ion conc.','DO (㎎/L)', 'TSI(Chl-a)','predict']) 

# print(mytestpd)


# mytestpd.to_csv("cor.csv")




# quit()
print(training_output)
my_model = build_anfis_model(training_input, output_size=2, neurons = 100)
my_model.fit(training_input, training_output, 
    epochs=3, batch_size=1, verbose=1, shuffle=True)

# model_json =  my_model.to_json()
# model_output = "model/rnn_model.json"
# weight_output = "model/rnn_model.h5"
# with open(model_output, "w") as json_file:
#         json_file.write(model_json)
#         # serialize weights to HDF5
#         my_model.save_weights(weight_output)
# quit()
# model_output = 'model/rnn_model.json'
# weight_output = 'model/rnn_model.h5'
# json_file = open(model_output, 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# my_model = model_from_json(loaded_model_json)
# my_model.load_weights(weight_output)

# print("_________________________")

# print(len(dictrictArr))
# print(len(myDf))

y_true = []

y_pred = []

finalArr = []
finalArr2 = []
for dictrict in dictrictArr:
    try:
        count = count + 1
        small_data = df[df['Name (E)']==dictrict]
        # print(len(small_data))
        small_data = small_data.drop('Name (E)', 1)
        timeframe = small_data['YY/MM'].values
        # print(small_data)
        split_date = "2016/04"


        training_set, test_set = small_data[small_data['YY/MM']<split_date], small_data[small_data['YY/MM']>=split_date]
        print(len(test_set))
        # continue
        training_set = training_set.drop('YY/MM', 1)
        test_set = test_set.drop('YY/MM', 1)
        training_set=training_set.astype('float')

        test_set=test_set.astype('float')

        
        LSTM_training_inputs = []
        for i in range(len(training_set)-window_len):
            temp_set = training_set[i:(i+window_len)].copy()
            for col in norm_cols:
                temp_set.loc[:, col] = temp_set[col]
                #print(temp_set)
            LSTM_training_inputs.append(temp_set)


        LSTM_test_inputs = []
        for i in range(len(test_set)-window_len):
            temp_set = test_set[i:(i+window_len)].copy()
            for col in norm_cols:
                temp_set.loc[:, col] = temp_set[col]
        # print(temp_set)
            LSTM_test_inputs.append(temp_set)
        
        LSTM_test_outputs = test_set['TSI(Chl-a)'][window_len:].values

        LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
        LSTM_training_inputs = np.array(LSTM_training_inputs)

        LSTM_test_inputs = [np.array(LSTM_test_inputs) for LSTM_test_inputs in LSTM_test_inputs]
        LSTM_test_inputs = np.array(LSTM_test_inputs)
        # print(LSTM_test_inputs)

        print(LSTM_test_inputs)
        predict =  my_model.predict(LSTM_test_inputs)
        # print("______________________________")
        # print(predict)
        # print("______________________________________")

        # quit()

        # print(len(predict))

        dates = [1,2,3,4,5,6,7,8]
        # fig, ax1 = plt.subplots(1,1)
        # print(LSTM_test_inputs)
        # print("***************************************")
        # print(predict)
        # print(test_set['TSI(Chl-a)'][window_len-1:].values)
        # print("____________________________________________________")
        # print(LSTM_test_outputs)
        predict_based_raw = test_set['TSI(Chl-a)'][window_len-1:].values
        predict_based = []
        for line in predict_based_raw:
            if line < 10:
                predict_based.append([1,0])
            elif line > 70:
                predict_based.append([0,1])
            else:
                temp = float(line-10)/70
                predict_based.append([1-temp,temp])

        print(predict)

        print(predict_based)

        if predict[-1][0] > predict[-1][1]:
            y_pred.append(1)
        else:
            y_pred.append(0)


        if predict_based[-1][0] > predict_based[-1][1]:
            y_true.append(1)
        else:
            y_true.append(0)



        # final_predict = []
        # final_predict.append(predict_based[1])

        loop = 0
        check = 0
        # for i in range(1, len(predict_based)):
        #   if predict_based[i] == predict_based[i-1]:
        #       loop = loop +1
        #       if loop > 1:
        #           check = 1
        #           continue
        #   if check == 1:
        #       continue
        # for i in range(1, len(predict)):
        #     temp = (1 + (predict[i]-predict[i-1])/predict[i-1])*predict_based[i-1]
        #     final_predict.append(temp)
        # print(final_predict)
        

        # mseValue = np.mean(np.abs((final_predict) - test_set['TSI(Chl-a)'][window_len:].values))/max(final_predict)
        
        # np.save('numpy/GRU/'+ dictrict+"_label", test_set['TSI(Chl-a)'][-10:].values)
        # np.save('numpy/GRU/'+ dictrict+"_prediction", final_predict[-10:])

        # # fig, ax1 = plt.subplots(1,1,figsize=(20,10))
        # ax1.plot(timeframe[:len(test_set['TSI(Chl-a)'][window_len:].values,)],test_set['TSI(Chl-a)'][window_len:].values, label='Actual')
        # ax1.plot(timeframe[:len(final_predict)],final_predict, label='Predicted')
        
        # ax1.plot(timeframe[-10:],test_set['TSI(Chl-a)'][-10:].values, label='Actual')
        # ax1.plot(timeframe[-10:],final_predict[-10:], label='Predicted')


        print("numpy save !!!!")
        
        # ax1.annotate('MAE: %.4f'%mseValue, 
        #   xy=(0.75, 0.9),  xycoords='axes fraction',
        #   xytext=(0.75, 0.9), textcoords='axes fraction')

        # # ax1.set_title("Dự đoán nổng độ tảo tại trạm "+dictrict,fontsize=13)
        # ax1.set_title("Chi-a Prediction at "+dictrict,fontsize=13)
        # ax1.legend()
        # fig.autofmt_xdate()
        # ax1.set_ylim(bottom=0)
        # ax1.set_ylim(top=100)
        # ax1.set_ylabel('gía cổ phiếu (VND)',fontsize=12)
        # ax1.xaxis.set_major_locator(loc)
        # ax1.xaxis.set_major_formatter(formatter)
        # ax1.xaxis.set_tick_params(rotation=10, labelsize=10)
        # ax1.set_ylim(bottom=0)
        # ax1.set_ylim(top=100)
        # # plt.show()
        # finalArr.append(final_predict[-2:])
        # finalArr2.append(test_set['TSI(Chl-a)'][window_len:].values[-2:])
        # dictrictName.append(dictrict)
        # dictrictMSE.append(mseValue)

        # plt.savefig("LSTM/"+ dictrict +'.png', dpi=100)
    #   # quit()
    except:
        continue

print("This is final report")
print(y_true)
print(len(y_true))
print(y_pred)
print(len(y_pred))

from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred))
quit()


for i in range(0, len(dictrictName)):
    print(dictrictName[i] + "||" + str(dictrictMSE[i]) + "|||")

df = pd.DataFrame(list(zip(dictrictName, dictrictMSE)), 
               columns =['Name', 'val']) 
df.to_csv("rnn.csv")

# 30-40 0,95-2,6    Hypolimia: 
# 40-50 2,6-7,3 Alpha- Mesotrophy
# 50-60 7,3-20  Beta- Mesotrophy
# 60-70 20-56   Eutrophy
# 70-80 56-155  Hypereutrophy
# >80   >155    Algae bloom

y_pred = []
print("final predict")
for i in range(0, len(dictrictName)):
    if finalArr[i][0] > 60 or finalArr[i][1] >60:
        y_pred.append(1)
    else:
        y_pred.append(0)
        # grade = "Eutrophy"
        # if finalArr[i][0] > 70 or finalArr[i][1] >70:
        #   grade = "Hypereutrophy"
        # if finalArr[i][0] > 80 or finalArr[i][1] >80:
        #   grade = "Algae bloom"
        # print("tram "+ dictrictName[i]+ " co kha nang no hoa")
        # print("Grade:" + grade) 

y_true  = []
print("final predict")
for i in range(0, len(dictrictName)):
    if finalArr2[i][0] > 60 or finalArr2[i][1] >60:
        y_true.append(1)
    else:
        y_true.append(0)
        # grade = "Eutrophy"
        # if finalArr2[i][0] > 70 or finalArr2[i][1] >70:
        #   grade = "Hypereutrophy"
        # if finalArr2[i][0] > 80 or finalArr2[i][1] >80:
        #   grade = "Algae bloom"
        # print("tram "+ dictrictName[i]+ " co kha nang no hoa")
        # print("Grade:" + grade) 

print(y_true)
print(len(y_true))
print(y_pred)
print(len(y_pred))

from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred))