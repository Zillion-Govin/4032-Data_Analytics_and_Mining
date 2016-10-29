# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:22:44 2016

@author: Stefan Setyadi
"""

import numpy as np
import pandas as pd
import time
from sklearn.metrics import mean_squared_error as mse

def cos_sim(matrix, epsilon=1e-9):
    sim = matrix.T.dot(matrix) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    #print(norms)
    return (sim/norms/norms.T)

def predict_wsum(ratings,similarity):
    #print(np.array([np.abs(similarity).sum(axis=1)]))
    return ratings.dot(similarity)/ np.array([np.abs(similarity).sum(axis=0)])
    
def predict_topk(ratings,similarity,k):
    pred = np.zeros(ratings.shape).astype(np.float32)
    topk = get_topk_pos(similarity,k)
    for i in range(len(topk)):
        new_sim = similarity[i,topk[i]]
        new_rating = ratings[:,topk[i]]
        pred[:,i] = new_rating.dot(new_sim)/np.array([np.abs(new_sim).sum(axis=0)])
    return pred
        
    
def get_mse(pred, actual):
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mse(pred, actual)    
    
def loadDF(pathName,name,cut_last=True):
    temp_df = pd.read_csv(pathName, sep=',', names=name)
    if(cut_last):
        temp_df.drop(name[-1:], axis=1, inplace=True)    
    return temp_df

def get_topk_pos(similarity,k):
    ## argpartition will return topk but not ordered
    return np.argpartition(-similarity,(0,k))[:,1:k+1]

def topk_mse(train,test,item_sim,k):
    k_mse = []
    starttime = time.time()
    for i in k:
        prediction = predict_topk(train,item_sim,i)
        #print(prediction[:4,:4])
        k_mse.append(get_mse(prediction,test))
        print("{} {}".format(i,time.time()-starttime))
        starttime=time.time()
    print(k_mse)

def topk_to_file(writePathName, item_sim,k):
    writeStr = []
    top10 = get_topk_pos(item_sim,k) # without the item itself
    for i in range(len(top10)):
        writeStr.append("{}:{}".format(index2_id[i],",".join([str(index2_id[j]) for j in top10[i]])))
    writeStr = "\n".join(writeStr)
    with open(writePathName, 'w') as writeFile:
        writeFile.write(writeStr)
        
trainingPathName = "./../dataset_partitioned/ratings_training.csv"
testPathName = "./../dataset_partitioned/ratings_test.csv"
headerName = ['user_id','item_id','rating','timestamp']

train_df = loadDF(trainingPathName,headerName)
test_df = loadDF(testPathName, headerName)
    
n_item = train_df.item_id.unique()
## create index between df index and raw item_id
index2_id = {}
id2_index = {}
for i in range(n_item.shape[0]):
    #print("{} {}".format(i,n_item[i]))
    index2_id[i] = n_item[i]
    id2_index[n_item[i]] = i

n_item = n_item.shape[0]
n_user = train_df.user_id.unique().shape[0]

#print("{} {}".format(n_user,n_item))

## fill up matrix with training data
train = np.zeros((n_user,n_item)).astype(np.float32)
for i in train_df.itertuples():
    #print( id2_index[i[2]])    
    train[i[1]-1, id2_index[i[2]]] = i[3]
print(train[:4,:4])

## create separate matrix to contain actual data (for testing)
test = np.zeros((n_user,n_item)).astype(np.float32)
for i in test_df.itertuples():
    #print( id2_index[i[2]])    
    test[i[1]-1, id2_index[i[2]]] = i[3]

sparsity = float(len(train.nonzero()[0])) / n_user / n_item * 100
print("Train Sparsity: {:6.2f}%".format(sparsity))
sparsity = float(len(test.nonzero()[0])) / n_user / n_item * 100
print("Test Sparsity: {:6.2f}%".format(sparsity))


item_sim = cos_sim(train)
#print(item_sim[:4,:4])

print(test[:4,:4])

k = [1,2,5,10,20,40,100,200]#,500]
#k = [3,4,5,6,7]

topk_mse(train,test,item_sim,k)

writePath = "top10.txt"
topk_to_file(writePath,item_sim,10)