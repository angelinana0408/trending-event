import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

print "*********************Parsing tweets***********************"

tweets_data_path = '../data/test_tweets.json'
file_name = '../data/tweets.csv'
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets = pd.DataFrame(index=list(range(0, len(tweets_data))),
                      columns=['created_at', 'tweetID', 'text', 'in_reply_to_screen_name',
                               'user_id_str', 'user_name', 'user_screen_name', 'user_description', 'user_verified',
                               'user_followers_count', 'user_friends_count', 'user_favourites_count',
                               'user_statuses_count',
                               'quote_count', 'reply_count', 'retweet_count', 'favorite_count', 'hashtags',
                               'user_mentions', 'retweeted_id', 'retweeted_text'])


def parseTweet(tweets, tweet, index):
    if 'created_at' not in tweet:
        return
    tweets.set_value(index, 'created_at', tweet['created_at'])
    tweets.set_value(index, 'tweetID', tweet['id_str'])
    tweets.set_value(index, 'text',
                     tweet['text'] if tweet['truncated'] == False else tweet['extended_tweet']['full_text'])
    tweets.set_value(index, 'in_reply_to_screen_name', tweet['in_reply_to_screen_name'])

    # use info
    tweets.set_value(index, 'user_id_str', tweet['user']['id_str'])
    tweets.set_value(index, 'user_name', tweet['user']['name'])
    tweets.set_value(index, 'user_screen_name', tweet['user']['screen_name'])
    tweets.set_value(index, 'user_description', tweet['user']['description'])
    tweets.set_value(index, 'user_verified', tweet['user']['verified'])
    tweets.set_value(index, 'user_followers_count', tweet['user']['followers_count'])
    tweets.set_value(index, 'user_friends_count', tweet['user']['friends_count'])
    tweets.set_value(index, 'user_favourites_count', tweet['user']['favourites_count'])
    tweets.set_value(index, 'user_statuses_count', tweet['user']['statuses_count'])

    tweets.set_value(index, 'quote_count', tweet['quote_count'])
    tweets.set_value(index, 'reply_count', tweet['reply_count'])
    tweets.set_value(index, 'retweet_count', tweet['retweet_count'])
    tweets.set_value(index, 'favorite_count', tweet['favorite_count'])

    tweets.set_value(index, 'hashtags', tweet['entities']['hashtags'])
    tweets.set_value(index, 'user_mentions', tweet['entities']['user_mentions'])
    # quote & reweet

    if 'quoted_status' in tweet:
        quoteTweet = tweet['quoted_status']
        tweets.set_value(index, 'retweeted_id', quoteTweet['id_str'])
        tweets.set_value(index, 'retweeted_text',
                         quoteTweet['text'] if quoteTweet['truncated'] == False else quoteTweet['extended_tweet'][
                             'full_text'])
    if 'retweeted_status' in tweet:
        reTweet = tweet['retweeted_status']
        tweets.set_value(index, 'retweeted_id', reTweet['id_str'])
        tweets.set_value(index, 'retweeted_text',
                         reTweet['text'] if reTweet['truncated'] == False else reTweet['extended_tweet']['full_text'])


index = 0

for tweet in tweets_data:
    parseTweet(tweets, tweet, index)
    index += 1

#tweets.to_csv(file_name, sep='\t', encoding='utf-8')
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('../data/tweets.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
tweets.to_excel(writer, sheet_name='Sheet1',encoding='utf-8')
# Close the Pandas Excel writer and output the Excel file.
writer.save()
print "**********Parsing tweets finished, stored in 'tweets.xlsx'***************"

