import util
import collections

filename = 'filteredRaw.txt'
n=3

with open(filename,'r') as myFile:
    doc = myFile.read().split("\n")

#cnt is counter for unique song player by each user
cnt = collections.Counter([i.partition("\t")[0] for i in doc]).items()

temp = sorted(cnt,key= lambda x: x[1])
temp = filter(lambda x: x[1]>=n,temp)
print len(temp)
temp = ["{}\t{}".format(i,j )for i,j in temp]
util.writeToFile("\n".join(temp),"newUserTrackcount.txt")
