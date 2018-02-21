import math
import numpy as np
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split
#-------------------------------------------------------------------
def log(n):
    return math.log(n)
#-------------------------------------------------------------------
def exp(n):
    return math.exp(n)
#-------------------------------------------------------------------
def applyZScore(dataframe):
    mean = np.mean(dataframe,axis=0)
    std = np.std(dataframe,axis=0)
    dataframe = (dataframe-mean)/std
    return dataframe
#-------------------------------------------------------------------

print "*********Classifing the dataset into sport_related or non_sport_related********"

## read train dataset
size=0
train_x=[]
train_y=[]
with  open("../data/classify_train.data",'r') as f:
        
    for line in f.readlines():
        items = line.split('\t')
        size = len(items)
        types = [float]* size
        data = [tp(item) for (tp, item) in zip(types,items)]
        #print type(data[0]),len(data)
        train_y.append(data[0])
        train_x.append(data[1:])

    #train_x =[line.split('\t') for line in f.readlines()]

parameters = [0.25]* size
    
## initialize training data
train_x =np.array(train_x)
#applyZScore(train_x)

train_x = np.insert(train_x,0,1,axis =1)


## read preprocessed dataset
test_x = []
tweetID = []

with  open("../data/preprocessed.data",'r') as f:

    for line in f.readlines():
        items = line.split('\t')
        size = len(items)
        types = [float]* size
        tweetID.append(items[0])
        data = [tp(item) for (tp, item) in zip(types,items)]
        test_x.append(data[1:])

test_x = np.array(test_x)
test_x = np.insert(test_x,0,1,axis =1)


## use logistic regression to classify dataset
classifier=LogisticRegression()
classifier.fit(train_x, train_y)
predictions=classifier.predict(test_x)

'''err_cnt=0
for i in range(len(predictions)):
    if predictions[i]!=train_y[i]:
        err_cnt+=1

print "accuracy",1-err_cnt/float(len(predictions))
'''

with open("../data/predictions.data",'w') as f:
    for p in predictions:
	f.write(str(p))
	f.write('\t')

predictions = []
with open("../data/predictions.data",'r') as f:

    items = f.read()
    items = items.split('\t')
    predictions = items


with open("../data/classified.data",'w') as f:
    for i in range(len(predictions)):
        if(predictions[i] == '1.0'):
	    f.write(str(tweetID[i]))
	    f.write('\t')
	    for item in test_x[i]:
	        f.write(str(item))
	        f.write('\t')
	    f.write('\n')
print "*********Classifing finished, stored in 'classified.data' ****************"
