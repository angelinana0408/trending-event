import math
import numpy as np
from sklearn.linear_model.logistic import LogisticRegression



## initialize parameters
size=0
train_x=[]
train_y=[]
with  open("../data/classify_train.data",'r') as f:
    for line in f.readlines():
        items = line.split('\t')
        size = len(items)
        types = [float]* size
        data = [tp(item) for (tp, item) in zip(types,items)]
        train_y.append(data[0])
        train_x.append(data[1:])

    
## initialize training data
dataframe =np.array(train_x)
train_x =np.insert(dataframe,0,1,axis =1)


## training and testing
#left=200
#right=800
classifier=LogisticRegression()
classifier.fit(np.array(list(train_x[0:600]) + list(train_x[800:])),np.array(list(train_y[0:600]) + list(train_y[800:])))
predictions=classifier.predict(train_x[600:800])

## evaluation
err_cnt=0
tp=0
fp=0
tn=0
fn=0
for i in range(len(predictions)):
    if predictions[i]!=train_y[i + 600]:
        err_cnt+=1
        if(predictions[i]==1):
            fp+=1
        else:
            fn+=1
    else:
        if(predictions[i]==1):
            tp+=1
        else:
            tn+=1
    
print "Accuracy",1-err_cnt/float(len(predictions))
precision = float(tp)/(tp+fp)
recall = float(tp)/(tp+fn)
print "Precision",precision,"Recall",recall
