import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print "**********************Preparing for Event Ranking ********************* Parsing total counts of tweets, including quote_count reply_count retweet_count favorite_count"

tweets_data_path = '../data/test_tweets.json'
file_name = '../data/tweetID_counts.csv'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

df_tweetID_counts = pd.DataFrame(index=list(range(0, len(tweets_data))),
                      columns=['tweetID', 'originalTweet_total_count','originalTweet_quote_count', 'originalTweet_reply_count',
                               'originalTweet_retweet_count', 'originalTweet_favorite_count'])

def parseTweet(df_tweetID_counts, tweet, index):
    if 'created_at' not in tweet:
        return
    df_tweetID_counts.set_value(index, 'tweetID', tweet['id_str'])
    quote_count = tweet['quote_count']
    reply_count = tweet['reply_count']
    retweet_count = tweet['retweet_count']
    favorite_count = tweet['favorite_count']
    # quote & reweet
    if 'quoted_status' in tweet:
        quoteTweet = tweet['quoted_status']
        quote_count += quoteTweet['quote_count']
        reply_count += quoteTweet['reply_count']
        retweet_count += quoteTweet['retweet_count']
        favorite_count += quoteTweet['favorite_count']
    '''if index == 2:
        print(tweet)'''
    if 'retweeted_status' in tweet:
        reTweet = tweet['retweeted_status']
        quote_count += reTweet['quote_count']
        reply_count += reTweet['reply_count']
        retweet_count += reTweet['retweet_count']
        favorite_count += reTweet['favorite_count']
    df_tweetID_counts.set_value(index, 'originalTweet_quote_count', quote_count)
    df_tweetID_counts.set_value(index, 'originalTweet_reply_count', reply_count)
    df_tweetID_counts.set_value(index, 'originalTweet_retweet_count', retweet_count)
    df_tweetID_counts.set_value(index, 'originalTweet_favorite_count', favorite_count)
    df_tweetID_counts.set_value(index, 'originalTweet_total_count', quote_count+reply_count+retweet_count+favorite_count)


index = 0
for tweet in tweets_data:
    parseTweet(df_tweetID_counts, tweet, index)
    index += 1

df_tweetID_counts.to_csv(file_name, sep='\t', encoding='utf-8')
