import numpy as np
import time
import pandas as pd
import io
import os
from scipy.spatial.distance import cosine

ENCODING = 'ASCII' ##File encoding
## loading source matrix
FILE_SOURCE = os.path.join('dataset_matrix', 'matrix.csv')

## convert the data matrix to panda dataframe
source = pd.read_csv(FILE_SOURCE, delimiter =',', encoding = ENCODING)

## path for output files
path_cosine = os.path.join('similarity_matrix', 'similarity_cosine.csv')
path_adjusted = os.path.join('similarity_matrix', 'similarity_adjusted_cosine.csv')
path_correlation = os.path.join('similarity_matrix', 'similarity_correlation.csv')

def cosine_similarity():
    ## open the file and put the data matrix into panda dataframe
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list() ## get the movie list
    ## create the dataframe for result
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    num_movie = len(indexing)
    
    ## calculating the cosine for each movie with other movie
    for i in range(0,num_movie):
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[[i,j],1:].T
            tempMatrix = tempMatrix.dropna(how='any')
            
            if(tempMatrix.empty):
                result = 0
            else:
                result = float("{0:.2f}".format(1-cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))
            df.iat[i,j] = result
            df.iat[j,i] = result
    create_file(df,path_cosine) ## write the result after finish calculating
        
def correlation_similarity():
    ## open the file and put the data matrix into panda dataframe
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list() ## get the movie list
    ## create the dataframe for result
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    sou = sou.set_index(indexing).T
    ## averrating for each item
    averrating = sou.iloc[1:,:].mean() 
    sou = sou.T.sub(averrating,axis='index').T

    num_movie = len(indexing)
    ## calculating the correlation similarity for each movie with other movie
    for i in range(0,num_movie):
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[1:,[i,j]]
            tempMatrix = tempMatrix.dropna(how='any')
            
            if(tempMatrix.empty):
                result = 0
            else:
                result = float("{0:.2f}".format(2-cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))/2
            df.iat[i,j] = result
            df.iat[j,i] = result
    create_file(df,path_correlation) ## write the result after finish calculating
    
def adjusted_cosine_similarity():
    ## open the file and put the data matrix into panda dataframe
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list() ## get the movie list
    ## create the dataframe for result
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    
    ## shrinkage of users rating
    num_movie = len(indexing)
    averrating = pd.Series(float(0), index = sou.columns)
    num_user = sou.shape[1]
    bu = sou.mean()
    print("user rating raw done")
    alpha = 1
    ru = pd.Series(float(0), index = sou.columns)
    total_valid= 0.0
    total_data = 0.0
    for i in range(1, num_user):
        ru.iat[i] = len(sou.iloc[:,i].dropna(how='any'))
        total_valid+= ru.iat[i]
        total_data += bu[i]*ru.iat[i]
    print("|RU| done")
    globalmean = total_data/total_valid
    print("global mean done")
    
    for i in range(1, num_user):
        averrating.iat[i]=alpha/(alpha+ru[i])*globalmean+ru[i]/(alpha+ru[i])*bu[i]
    print("normalized user rating done")
    ## calculating the adjusted cosine similarity
    for i in range(0,num_movie):
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[[i,j],1:].T.sub(averrating,axis='index').dropna(how='any')
            
            if(tempMatrix.empty):
                result = 0
            else:
                result = float("{0:.2f}".format(2-cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))/2
            df.iat[i,j] = result
            df.iat[j,i] = result

    create_file(df,path_adjusted) ## write out the adjusted cosine result
                
def create_file(data,path):
    ## write to file and if file initially not there, create a new one
    if not os.path.exists(path):
        with io.open(path,'w+',encoding = ENCODING):
            print ("creating file...")
    data.to_csv(path, encoding=ENCODING)
    print ('finish')

def get_list():
    movie_list = source.iloc[:,0]
    return (movie_list)

    
