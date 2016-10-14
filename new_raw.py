with open("new_user.txt",'r') as myFile:
    new_user = set(myFile.read().split("\n"))
with open("user-id artist_id track-id playcount.txt",'r') as myFile:
    raw_data = myFile.read().split("\n")[1:]
raw_data = [i.partition("\t") for i in raw_data]
print len(raw_data)
raw_data = ["".join(i) for i in raw_data if i[0] in new_user]
print len(raw_data)

with open("new_raw.txt",'w') as newFile:
    newFile.write("\n".join(raw_data))
