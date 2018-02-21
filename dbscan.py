from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.decomposition import TruncatedSVD
import numpy as np
from scipy import sparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#Read data to obtain features
print "***************Clustering dataset with DBSCAN****************"
print "Reading data from 'classified.data'"
features=[]
tweetID=[]
with open("../data/classified.data",'r') as f:
    for l in f.readlines():
        data = l.strip().split()
        tweetID.append(data[0])
        data = [float(item) for item in data]
        features.append(data[1:])
features = np.array(features)
Sfeatures = sparse.csr_matrix(features)

#Dimension Reduction
print "Dimension reduction on features(from 4000 d to 200 d), about 1-3 minutes"
features = TruncatedSVD(n_components=200, n_iter=500).fit_transform(Sfeatures)
features_3d = TruncatedSVD(n_components=3, n_iter=500).fit_transform(Sfeatures)
print "Finish dimension reduction"

#DBSCAN
print "Dbscan on reduced features, about 1-3 minutes"
dbscan = DBSCAN(eps=0.8, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=1)
prediction = dbscan.fit_predict(features, y=None, sample_weight=None)

with open("../data/clustered_dbscan.data",'w')as f:
    for (tid,label) in zip(tweetID,prediction):
        f.write("{} {}\n".format(tid,label))
        

#Plot 3D image     
xvals={}
yvals={}
zvals={}

for p in set(prediction):
    xvals[p]=[]
    yvals[p]=[]
    zvals[p]=[]
color = ['r','b','g','y','w','k','c','m']
for (xy,p) in zip(features_3d, prediction):
    xvals[p].append(xy[0])
    yvals[p].append(xy[1])
    zvals[p].append(xy[2])

sortedkeys=sorted(xvals, key=lambda x:len(xvals[x]),reverse=True)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

i=0
for p in sortedkeys[0:7]:
    if p==-1:
        continue
    ax.scatter(xvals[p], yvals[p], zvals[p], c=color[i], marker='o')
    i+=1
    
#plt.show()
print "Plot the cluster figure and save it to 'dbscan.pnd'"
plt.savefig("../data/dbscan.png")

print "Finish dbscan, write result to 'clustered_dbscan.data' and 'dbscan.png' "

