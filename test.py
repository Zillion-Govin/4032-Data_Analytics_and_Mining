import pandas
from scipy.spatial.distance import cdist
from scipy.spatial.distance import cosine
# # a = pandas.read_csv('matrix.csv')
# a = {'col1':[1,2],'col2':[3,4],'col3':[5,6]}
# df = pandas.DataFrame(a)
# lst = list(df.columns)
# # print df[lst].values.T
# # print df.values
# print df.values.T
# item = df.values.T
# item1 = df.iloc[0].values
# item2 = df.loc[1].values
# for i in xrange(0,3):
#     print item1[i]
#     print item2[i]
#     print cosine(item1,item2)
# print cdist(item,item,'cosine')
# print cdist(item1,item2,'cosine')

a = pandas.read_csv('similarity_cosine.csv',header=0,index_col=0)
df =pandas.DataFrame(a.loc[2031])
print df
df.to_csv("1.tsv")
