import io
import re

#already randomize the song
doc = io.open("nourl_randomized.tsv",'r',encoding='utf-8').readlines()

training = io.open("training.tsv",'a',encoding='utf-8')
test = io.open("test.tsv",'a',encoding='utf-8')

userSongCount = [0] * 1000 # counter for each user-song-artist

# function to get user id
def getUserId(row):
    user = row.split("\t",1)[0]
    userId = int(user.split("_")[1])
    return userId

# counter for userSongCount
for i in doc:
    userId = getUserId(i)
    userSongCount[userId - 1] += 1

print userSongCount

# split based on 80 - 20
currentUserId = 1;
currentUserIndex = 1;
print currentUserId + " started"

for i in doc:
    userId = getUserId(i)
    if(currentUserId != userId):
        print str(userId) + " started"
        currentUserId = userId
        currentUserIndex = 1

    if (currentUserIndex <= (0.8 * userSongCount[userId-1])): # 0.8 goes to training
        training.write(i)
    else:
        test.write(i)

    currentUserIndex += 1
