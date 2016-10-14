with open("user_id trackcount.txt",'r') as myFile:
    doc = myFile.read().split('\n')

playcount = [i.partition("\t") for i in doc[1:]]
print len(playcount)
new_user = [i[0] for i in playcount if i[2] not in '12']

with open("new_user.txt",'w') as new_user_file:
    new_user_file.write("\n".join(new_user))
