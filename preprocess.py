import pandas as pd
import csv
import xlrd
import re
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#df_rawText = pd.read_csv('tweets_test.csv')

df_rawData = pd.read_excel('../data/preprocess_train.xlsx', encoding='utf-8')

print "*********************Preprocessing the dataset*********************"
print "Using TF-IDF to convert text to vector, about 3 minutes"
text_alphanumeric = np.empty([df_rawData.shape[0],], dtype="S1000")
has_http=list()
for index in range(df_rawData.shape[0]):
    text = unicode(df_rawData.loc[df_rawData.index[index], 'text'])
    if(text.find('RT') > -1):
        text=text.split(":")[0]
        retweet = df_rawData.loc[df_rawData.index[index], 'retweeted_text']
        text+=' '+unicode(retweet)

    if (text.find('https:') > -1):#feature  has_http
        has_http.append(1)
    else:
        has_http.append(0)

    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z ]+', '',text, flags=re.MULTILINE)
    #text = regex.sub('[^a-zA-Z]', text)
    #regex = re.compile()
    # First parameter is the replacement, second parameter is your input string
    #text = regex.sub(' ', text)

    # Out: 'abdE'
    text_alphanumeric[index] = text

df_rawData2 = pd.read_excel('../data/tweets.xlsx', encoding='utf-8',converters={'tweetID':str})

text_alphanumeric2 = np.empty([df_rawData2.shape[0],], dtype="S1000")
has_http2=list()
tweetID=list()
for index in range(df_rawData2.shape[0]):
    text = unicode(df_rawData2.loc[df_rawData2.index[index], 'text'])
    tid=unicode(df_rawData2.loc[df_rawData2.index[index], 'tweetID'])
    tweetID.append(tid)
    if(text.find('RT') > -1):
        text=text.split(":")[0]
        retweet = df_rawData2.loc[df_rawData2.index[index], 'retweeted_text']
        text+=' '+unicode(retweet)  #to combine text and retweet text

    if (text.find('https:') > -1):
        has_http2.append(1)
    else:
        has_http2.append(0)

    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z ]+', '',text, flags=re.MULTILINE)


    # Out: 'abdE'
    text_alphanumeric2[index] = text



label = df_rawData['label']
#df1['text_alphanumeric'] = Series(np.random.randn(sLength), index=df1.index)
d_label_text = {'label': label, 'text_alphanumeric': text_alphanumeric}
df_label_text = pd.DataFrame(data=d_label_text)

#df1['text_alphanumeric'] = Series(np.random.randn(sLength), index=df1.index)
d_label_text2 = { 'text_alphanumeric': text_alphanumeric2}
df_label_text2 = pd.DataFrame(data=d_label_text2)


#######run tfidf##########
corpus = df_label_text['text_alphanumeric']
corpus2 = df_label_text2['text_alphanumeric']
vectorizer = TfidfVectorizer()
X_train=vectorizer.fit_transform(corpus)
X_test=vectorizer.transform(corpus2)
X=X_test.toarray()
file_object = open('../data/preprocessed.data',"w")
for i in range(X.shape[0]):
    #weight_array.append(weight_temp)
    file_object.write(str(tweetID[i]) + '\t' + str(has_http2[i]) + '\t')
    for j in range(X.shape[1]-1):
        #print(i, j)
        file_object.write(str(X[i][j])+'\t')
    file_object.write(str(X[i][X.shape[1]-1]) + '\n')

file_object.close()

print "*******Preprocessing finished, stored in 'preprocessed.data'*************"


