with open("matrix.txt",'r') as myFile:
    doc = myFile.read().split('\n')
doc = [i.split(',') for i in doc]

num_song = len(doc)
cosineSim = [[-100 for i in range(num_song)] for j in range(num_song)]
##absolVal = [0 for i in range(num_song)]
num_user = len(doc[0])

print(num_song)
print(num_user)
##print(num_user)
for i in range(1,num_song):
    for j in range(i,num_song):
        temp = 0.0
        tempI = 0.0
        tempJ = 0.0
        for k in range(1,num_user):
            if((int(doc[i][k]) == 0) or (int(doc[j][k]) == 0)):
                pass
            else:
                temp += float(doc[i][k])*float(doc[j][k])
                tempI += float(doc[i][k])**2
                tempJ += float(doc[j][k])**2
        if(tempI == 0 or tempJ == 0):
            cosineSim[i][j] = -10
            cosineSim[j][i] = -10
        else:
            cosineSim[i][j] = float("{0:.2f}".format(temp/((tempI**0.5)*(tempJ**0.5))))
            cosineSim[j][i] = cosineSim[i][j]
    print("i :" + str(i) )
    cosineSim[i][0] = cosineSim[0][i] = doc[i][0]        

##for i in range(0,num_song):
##    print(cosineSim[i])

##correlationSim = [[-100 for i in range(num_song)] for j in range(num_song)]
##
##averRating = [0 for i in range(num_song)]
##for i in range(1,num_song):
##    for j in range(1,num_user):
##        averRating[i] += float(doc[i][j]) 
##    averRating[i] = averRating[i]/(num_user-1)
##    
##for i in range(1,num_song):
##    for j in range(i,num_song):
##        totaltemp = 0.0
##        totaltempUI =0.0
##        totaltempUJ =0.0
##        for k in range(1,num_user):
##            tempUI = float(doc[i][k]) - averRating[i]
##            tempUJ = float(doc[j][k]) - averRating[j]
##            totaltemp += tempUI*tempUJ
##            totaltempUI += tempUI**2
##            totaltempUJ += tempUJ**2
##        correlationSim[i][j] = float("{0:.2f}".format((totaltemp/((totaltempUI**0.5)*(totaltempUJ**0.5))+1)/2))
##        correlationSim[j][i] = correlationSim[i][j]
##    correlationSim[i][0] = correlationSim[0][i] = doc[i][0]        
##
##for i in range(0,num_song):
##    print(correlationSim[i])
