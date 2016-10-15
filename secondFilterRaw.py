filename = "filteredRaw.txt"

with open("newUserTrackCount.txt",'r') as myFile:
    user_list = set([i.partition("\t")[0] for i in myFile.read().split("\n")])

with open(filename,'r') as myFile:
    triplet = myFile.read().split("\n")

triplet = filter(lambda x: x.partition("\t")[0] in user_list,triplet)
print len(triplet)

writeString = "\n".join(triplet)
with open('secondFilteredRaw.txt','w') as newFile:
    newFile.write(writeString)
