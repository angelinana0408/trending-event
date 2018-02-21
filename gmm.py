from sklearn.mixture import GMM
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


import math
import random
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD

print "***************Clustering dataset with GMM, about 7 minutes**************"

def tsne(data,toDimention):
    reduced = TSNE(n_components=toDimention, perplexity=40,verbose=0, n_iter_without_progress=500).fit_transform(data)
    return reduced
#visualize the 2D

def SVD(data,toDimention):
    reduced = TruncatedSVD(n_components=toDimention,n_iter=500).fit_transform(data)
    return reduced


def plotting(clusters, data, num):
    size = num
    labelColor = []
    for i in range(0, size):
        r = lambda: random.randint(0, 255)
        labelColor.append("#%02X%02X%02X" % (r(), r(), r()))
    for i in range(0,data.shape[0]):
        plt.scatter(data[i][0], data[i][1], color=labelColor[clusters[i]])
    plt.show()

def plotting_3d(clusters, data, num):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    size = num
    labelColor = []
    for i in range(0, size):
        r = lambda: random.randint(0, 255)
        labelColor.append("#%02X%02X%02X" % (r(), r(), r()))
    for i in range(0,data.shape[0]):
        ax.scatter(data[i][0], data[i][1], data[i][2],c=labelColor[clusters[i]])

    #plt.show()
    plt.savefig('../data/GMM.png')


test_x = []
tweetID = []

with  open("../data/classified.data",'r') as f:

    for line in f.readlines():
        items = line.split('\t')
        items = items[:-1]

        size = len(items)
        types = [float]* size
        data = [tp(item) for (tp, item) in zip(types,items)]
        test_x.append(data[1:])

        size_id=1
        types_id=[str]* size_id
        data_id = [tp(item) for (tp, item) in zip(types_id, items)]
        tweetID.append(data_id[0])



a=np.array(test_x)
k=np.isfinite(a).all()
X = SVD(a,200)
X_plot = SVD( np.array(test_x),3)
component=5
gmm = GMM(n_components=component).fit(X)
labels = gmm.predict(X)

plotting_3d(labels,X_plot,component)

file_object = open('../data/clustered_GMM.data',"w")
for i in range(X.shape[0]):
    #weight_array.append(weight_temp)
    file_object.write((tweetID[i]) + ' ' + str(labels[i]) + '\n')
file_object.close()

print "Finish GMM, write result to 'clustered_GMM.data' and 'GMM.png' "
