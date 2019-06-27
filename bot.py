import json
import nltk
import datetime
import time
from twython import TwythonStreamer  
from twython import Twython  

def bigram_poem(phrase):                                                  # define new function bigram_poem   
    rejects = '¿.?!,[]|"“();…{}«•*+$'                                      # define punctuation to be removed
    phrase_reject = phrase.translate({ord(c): None for c in rejects})     # remove defined punctuation
    phrase_split = phrase_reject.split(' ')                               # split phrase by whitespace
    phrase_clear = list(filter(None, phrase_split))                       # strip any extra whitespace
    phrase_shortened = phrase_clear[0:8]                                  # only use the first 8 terms
    phrase_bigram = list(nltk.bigrams(phrase_shortened))                  # convert to bigram list
    tw = ''                                                               # create new string
    for b in phrase_bigram:                                               # loop through bigrams
        tw += ' ' + b[0] + ' ' + b[1] + ' \n'                             # add looped bigrams to string w line break
    return(tw)

with open("twitter_credentials.json", "r") as file:                       # load credentials from json file (not included for security reasons)
    creds = json.load(file)

twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],  
                    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])        # add credentials to access API

class MyStreamer(TwythonStreamer):                                        # create a class that inherits TwythonStreamer
    
    def on_success(self, data):                                           # receive data when successful
                                                                          # Conditions: 1) restrict tweets to 3 or more words, 
        tweet = data['text']                                              #    2) exclude retweets, 3) exclude links, 
        bigram_len = bigram_poem(tweet).count('\n')                       #    4) English only, 5-6) exclude defined users
        if 'text' in data and bigram_len > 2 \
        and 'RT' not in tweet \
        and 'http' not in bigram_poem(tweet) \
        and data['lang'] == 'en' \
        and data['user']['screen_name'] != 'BigramPoetry' \
        and data['user']['screen_name'] != 'sodnpoo_cams':
            tweet = tweet.replace('\n',' ').replace('VIDEO','')           # remove edge cases with bad formatting
            tweet = tweet.replace(' -',' ').replace(' –',' ').replace(' ‘','')
            tweet = tweet.replace('- ',' ').replace(' /',' ').replace('— ',' ')
            tweet = tweet.replace('&amp','and').replace('&at','').replace('&gt','')
            tweet = tweet.replace(': ',' ').replace(':)','')
            poem = 'A Bigram Poem inspired by ' + data['user']['name'] 
            poem += ':' + '\n' + bigram_poem(tweet)                       # use bigram_poem function and title line
            twitter.update_status(status=poem)                            # tweet out on @BigramPoetry account
            print(poem)                                                   # print result, timestamp (for testing)
            print(datetime.datetime.now(), '\n')
            self.disconnect()                                             # stop stream (so old tweets don't dam up)
    
    def on_error(self, status_code, data):                                # when problem with the API
        print(status_code, data)
        print(datetime.datetime.now())
        self.disconnect()

stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],      # credentials for API streaming
                    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

while True:                                                               # continuosly runs the function
    status_stream = stream.statuses.filter(track='machine learning')      # start the stream to search for tweet
    time.sleep(600)                                                       # waits 10 minutes (600 seconds) before starting over
