import pandas
import numpy

def validate():
    total = 0
    validation_data = pandas.DataFrame.from_csv("matrix.csv",encoding='utf-8')
    with open('test_file.csv','r') as test_data:
        for i,lines in enumerate(test_data,1):
            line = lines.split(',')
            matrix = validation_data.loc[int(line[2]),line[1]]
            sums = numpy.square(matrix - int(line[3]))
            total += sums
        value = numpy.divide(total, i)
        print value

validate()