import io
import re

#already randomize the movie
doc = io.open("ratings_randomized.txt",'r',encoding='utf-8').readlines()

training = io.open("ratings_training.txt",'a',encoding='utf-8')
test = io.open("ratings_test.txt",'a',encoding='utf-8')

userRatingCount = [0] * 6040 # counter for each user
movieRatingCount = [0] * 4000 # counter for each movie

# function to get user id
def getUserId(row):
    userId = int(row.split("::")[0])
    return userId

# function to get movie id
def getMovieId(row):
    movieId = int(row.split("::")[1])
    return movieId

index = 0;
# counter for user & movie count
for i in doc:
    index += 1
    userId = getUserId(i)
    movieId = getMovieId(i)
    userRatingCount[userId - 1] += 1
    movieRatingCount[movieId - 1] += 1

lastUserIndex = 0;
lastUserId = 0;
currentUserId = 0;
currentUserIndex = 1;

index = 0;
for i in doc:
    userId = getUserId(i)
    movieId = getMovieId(i)

    if(currentUserId != userId):
        print "Change User ID to " + str(userId)
        currentUserId = userId
        currentUserIndex = 1
        lastUserIndex = index
    if(currentUserIndex <= (0.8 * userRatingCount[userId-1])):
        movieRatingCount[movieId-1] -= 1;
        currentUserIndex += 1
        training.write(i)
    else:
        
        if(movieRatingCount[movieId-1] <= 1):
            movieRatingCount[movieId-1] -= 1;
            training.write(i)
        else:
            movieRatingCount[movieId-1] -= 1;
            currentUserIndex += 1
            test.write(i)
    index += 1;
