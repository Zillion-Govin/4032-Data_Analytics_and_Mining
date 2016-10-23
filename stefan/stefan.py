# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:22:44 2016

@author: Stefan Setyadi
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error as mse

def cos_sim(matrix, epsilon=1e-9):
    sim = matrix.T.dot(matrix) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    #print(norms)
    return (sim/norms/norms.T)

def predict_wsum(ratings,similarity):
    #print(np.array([np.abs(similarity).sum(axis=1)]))
    return ratings.dot(similarity)/ np.array([np.abs(similarity).sum(axis=1)])
    
#change later to load from file
def train_test_split(ratings):
    test = np.zeros(ratings.shape)
    train = ratings.copy()
    for user in range(ratings.shape[0]):
        test_ratings = np.random.choice(ratings[user, :].nonzero()[0], 
                                        size=10, 
                                        replace=False)
        train[user, test_ratings] = 0.
        test[user, test_ratings] = ratings[user, test_ratings]
        
    # Test and training are truly disjoint
    assert(np.all((train * test) == 0)) 
    return train, test    
    
def get_mse(pred, actual):
    # Ignore nonzero terms.
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mse(pred, actual)    
    
pathName = "ratings.csv"
names = ['user_id','item_id','rating','timestamp']
df = pd.read_csv(pathName, sep=',', names=names)
df.drop('timestamp',axis=1,inplace=True)
    
n_item = df.item_id.unique()
index2_id = {}
id2_index = {}
for i in range(n_item.shape[0]):
    #print("{} {}".format(i,n_item[i]))
    index2_id[i] = n_item[i]
    id2_index[n_item[i]] = i

n_item = n_item.shape[0]
n_user = df.user_id.unique().shape[0]

#print("{} {}".format(n_user,n_item))


mat = np.zeros((n_user,n_item))
for i in df.itertuples():
    #print( id2_index[i[2]])    
    mat[i[1]-1, id2_index[i[2]]] = i[3]
print(mat[:4,:4])

sparsity = float(len(mat.nonzero()[0])) / n_user / n_item * 100
print("Sparsity: {:6.2f}%".format(sparsity))

train,test = train_test_split(mat)

item_sim = cos_sim(train)
print(item_sim[:4,:4])

prediction = predict_wsum(train,item_sim)
print(prediction[:4,:4])

print(get_mse(prediction,test))
