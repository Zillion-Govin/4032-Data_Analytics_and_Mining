import numpy as np
import pandas as pd
import io
import os
from scipy.spatial.distance import cosine

ENCODING = 'ASCII'
FILE_SOURCE = 'matrix.csv'
source = pd.read_csv(FILE_SOURCE, delimiter =',', encoding = ENCODING)
path = os.path.join('D:\\', 'CZ4032', 'similarity_matrix_answer.csv')

def cosine_similarity():
    sou = pd.read_csv(FILE_SOURCE, delimiter = ',' , encoding = ENCODING)
    indexing = get_list()
    df = pd.DataFrame(float(0), index = indexing, columns = indexing)
    num_movie = len(indexing)
    for i in range(0,num_movie):
        for j in range(i,num_movie):
            tempMatrix = sou.iloc[[i,j],1:].T
            tempMatrix = tempMatrix.loc[(tempMatrix!=0).all(axis=1)]
            """if(tempI == 0 or tempJ == 0):
                cosineSim[i][j] = -10
                cosineSim[j][i] = -10
            else:
                cosineSim[i][j] = float("{0:.2f}".format(temp/((tempI**0.5)*(tempJ**0.5))))
                cosineSim[j][i] = cosineSim[i][j]"""
            result = float("{0:.2f}".format(1- cosine(tempMatrix.iloc[:,0],tempMatrix.iloc[:,1])))
            if(result == np.nan):
                result = 0
            df.iat[i,j] = result
            df.iat[j,i] = result
        print(i)
    create_file(df,path)

    
def create_file(data,path):
    if not os.path.exists(path):
        with io.open(path,'w+',encoding = ENCODING):
            print ("creating file...")
    data.to_csv(path, encoding=ENCODING)
    print ('finish')

def get_list():
    movie_list = source.iloc[:,0]
    return (movie_list)

    
    
