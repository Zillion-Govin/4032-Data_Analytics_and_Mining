import numpy
import pandas
import io
import os
from sklearn.cross_validation import train_test_split

ENCODING = 'ASCII'
FILE_PATH_TRAIN = 'dataset_matrix\\matrix.csv'
FILE_PATH_TEST = 'dataset_matrix\\matrix_test.csv'
TRAIN_SOURCE = 'dataset_partitioned\\ratings_training.dat'
TEST_SOURCE = 'dataset_partitioned\\ratings_test.dat'

# generate the list for movie and user from the source to be used as a column and row for the matrix
def get_list(path):
    movie_list ={}
    user_list = {}
    with io.open(path, 'r', encoding=ENCODING) as source:
        for lines in source:
            line = lines.strip().split('::')
            movie_list[line[1]] = 0
            user_list[line[0]] = 0
    return movie_list,user_list

# create the file for the matrix, if its not exist then it will create the file first
def create_file(data,path):
    if not os.path.exists(path):
        with io.open(path,'w+',encoding = ENCODING):
            print "creating file..."
    data.to_csv(path, encoding=ENCODING)
    print 'finish'

# create the matrix based on the source list
def create_matrix(path,dest):
    movie_list,user_list = get_list(path)
    # create the dataframe based on the lists provided with uint8 data type to save the size of the matrix
    data = pandas.DataFrame(0,columns=user_list.keys(),index=movie_list.keys(),dtype='uint8')
    with io.open(path, 'r', encoding=ENCODING) as source:
        for i, lines in enumerate(source, 0):
            line = lines.split('::')
            data.loc[line[1]][line[0]] = int(line[2])
    data.replace(0, numpy.NaN, inplace=True)
    create_file( data= data,path=dest)

# change the path and dest to test path if wanted to create test matrix
if __name__ == "__main__":
    create_matrix(path = TRAIN_SOURCE,dest = FILE_PATH_TRAIN)