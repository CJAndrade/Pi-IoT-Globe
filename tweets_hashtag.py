#!/usr/bin/python
#Create for the for the Pi IoT Globe project- to get tweets for a specific hastag
#Author : @CarmelitoA 06/23/2017
#Based on the tweepy libary http://www.tweepy.org/
#Prerequisite ::  sudo pip install tweepy
import tweepy
import re,string
#Update you application details from https://dev.twitter.com/
consumer_key = "xxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_key = "xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#Update the hastag to the one you plan to track
hashTag = "RaspberryPiZero" 

OAUTH_KEYS = {'consumer_key':consumer_key, 'consumer_secret':consumer_secret,
              'access_token_key':access_token_key, 'access_token_secret':access_token_secret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)
getTweet = tweepy.Cursor(api.search, q=hashTag).items(30)

#Filtering the un-readable things in the tweet.text
def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

file = open("tweets.txt","w")
for tweet in getTweet:
    #filtering tweets in english(en), and also filtering retweets (RT @) based on tweepy docs
    if tweet.lang == 'en' and 'RT @' not in tweet.text:
        fileText = 'From '+ tweet.author.name.encode('utf8') + ' the tweets reads ' + strip_all_entities(strip_links(tweet.text.encode('utf8'))) + "  "
        # added encode('utf8') to resolve the encoding error on some tweets
        file.write(fileText)
        print fileText
        print "Name:", tweet.author.name.encode('utf8') #this is what we need
        print "Screen-name:", tweet.author.screen_name.encode('utf8')
        print "Tweet created:", tweet.created_at
        print "Tweet:", tweet.text.encode('utf8') #this is what we need to apply a filter
        #print "Retweeted:", tweet.retweeted
        #print "Favourited:", tweet.favorited
        #print "Location:", tweet.user.location.encode('utf8')
        #print "Time-zone:", tweet.user.time_zone
        #print "Geo:", tweet.geo
        print "-------------------------------"
file.close()
