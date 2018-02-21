import pandas as pd
import numpy as np

print "***********Generating summary of each cluster and Ranking clusters************"

def readDataSet_excel(filePath, fields):
    df_rawData = pd.read_excel(filePath,usecols=fields,encoding='utf-8',converters={'tweetID':str})
    return df_rawData

def readDataSet_from_csv(filePath):
    dataSet = []
    with open(filePath) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    index = 0
    for line in lines:
        content_a_line = line.split('\t')
        if index == 0:
            header = content_a_line
        else:
            dataSet.append(content_a_line[1:])
        index += 1
    df = pd.DataFrame(dataSet, columns=header)
    return df

def readDataSet_from_data(filePath, header):
    dataSet = []
    with open(filePath) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    index = 0
    for line in lines:
        content_a_line = line.split(' ')
        dataSet.append(content_a_line)
    df = pd.DataFrame(dataSet, columns=header)
    return df

for clusterFileName in ['../data/clustered_GMM.data','../data/clustered_dbscan.data']:
    #original tweet(unclassified)
    fields1 = ['tweetID','text']
    df_tweetID_text = readDataSet_excel('../data/tweets.xlsx',fields1)
    #df_tweetID_text = df_tweet[fields1]
    fields2 = ['tweetID', 'originalTweet_total_count']
    df_tweetID_counts = readDataSet_from_csv('../data/tweetID_counts.csv')
    df_tweetID_totalCounts = df_tweetID_counts[fields2]
    tweetID_column_text = df_tweetID_text['tweetID'].tolist()
    tweetID_column_totalCounts = df_tweetID_counts['tweetID'].tolist()
    #classifed tweets dataset with clusterID
    header = ['tweetID','clusterID']
    df_tweetID_clusterID = readDataSet_from_data(clusterFileName,header)
    #df_tweetID_clusterID = readDataSet_from_data('clustered_dbscan.data',header)
    #print(df_tweetID_clusterID)
    clusterID_column = df_tweetID_clusterID['clusterID'].tolist()
    clusterID, indices = np.unique(clusterID_column, return_index=True)
    clusterNum = len(clusterID)
    #print(clusterNum)
    #print(clusterID)
    #result dataframe
    df_joint = pd.DataFrame(index=list(range(0, clusterNum)),
                          columns=['clusterID', 'totalCount','topTweetID','topTweetText', 'topTweetText_count'])
    for clusterIndex in range(clusterNum):
        tweetCount = 0
        totalCount = 0
        topTweetText_count = 0
        textBag = set()
        df_joint.set_value(clusterIndex, 'clusterID', clusterID[clusterIndex])
        print("===================================cluster",clusterID[clusterIndex])
        for dataIndex in range(len(df_tweetID_clusterID)):
            if df_tweetID_clusterID.iloc[dataIndex]['clusterID'] == clusterID[clusterIndex]:
                tweetCount += 1
                tweetID = df_tweetID_clusterID.iloc[dataIndex]['tweetID']
                index_in_textDF = tweetID_column_text.index(tweetID)
                index_countsDF = tweetID_column_totalCounts.index(tweetID)
                current_text = df_tweetID_text.iloc[index_in_textDF]['text']
                if current_text not in textBag:
                    textBag.add(current_text)
                    current_tweet_count = df_tweetID_totalCounts.iloc[index_countsDF]['originalTweet_total_count']
                    totalCount += int(current_tweet_count)
                    #print('text', current_text)
                    #print('totalcount', current_tweet_count)
                    if current_tweet_count>topTweetText_count:
                        df_joint.set_value(clusterIndex, 'topTweetText_count', current_tweet_count)
                        df_joint.set_value(clusterIndex, 'topTweetText', current_text)
                        df_joint.set_value(clusterIndex, 'topTweetID', tweetID)
                        topTweetText_count = current_tweet_count
        df_joint.set_value(clusterIndex, 'totalCount', totalCount)
        #print("pure tweets number in cluster: ",tweetCount, totalCount)

    #print(df_joint)

    sorted_df_joint = df_joint.sort_values('totalCount', ascending = 0)
    #print(sorted_df_joint)
    print("===================ranking========================")
    print("Got "+str(clusterNum)+" clusters:")
    for index in range(len(sorted_df_joint)):
        clusterID = sorted_df_joint.iloc[index]['clusterID']
        topTweet = sorted_df_joint.iloc[index]['topTweetText']
#       print("@@@@@@@cluster"+str(clusterID)+": "+topTweet)

    if clusterFileName == '../data/clustered_GMM.data':
        #sorted_df_joint.to_csv('../data/GMM_Ranking.csv', sep='\t', encoding='utf-8')
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('../data/GMM_Ranking.xlsx', engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        sorted_df_joint.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        print "Ranking finished, final result is stored in GMM_Ranking.xlsx"
    if clusterFileName == '../data/clustered_dbscan.data':
        #sorted_df_joint.to_csv('dbscan_Ranking.csv', sep='\t', encoding='utf-8')
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('../data/dbscan_Ranking.xlsx', engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        sorted_df_joint.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        print "Ranking finished, final result is stored in dbscan_Ranking.xlsx"

