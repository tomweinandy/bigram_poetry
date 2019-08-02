#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import nltk
import datetime
import random
import time
from twython import TwythonStreamer
from twython import Twython
import sys

def bigram_poem(phrase):                                              # define new function bigram_poem
    rejects = '¿.?!,[]|"“”’();…{}«•*+@~<>'                            # define punctuation to be removed
    phrase_reject = phrase.translate({ord(c): None for c in rejects}) # remove defined punctuation
    phrase_split = phrase_reject.split(' ')                           # split phrase by whitespace
    phrase_clear = list(filter(None, phrase_split))                   # strip any extra whitespace
    phrase_shortened = phrase_clear[0:8]                              # only use the first 8 terms
    phrase_bigram = list(nltk.bigrams(phrase_shortened))              # convert to bigram list
    tw = ''                                                           # create new string
    for b in phrase_bigram:                                           # loop through bigrams
        tw += ' ' + b[0] + ' ' + b[1] + ' \n'                         # add looped bigrams to string w line break
    return(tw)

### For testing function ###
AD = ['I hear the jury’s still out on science.', 'I’m a monster!', 'Baby you got a stew going.', 'Do these effectively hide my thunder?', 'Army had a half day.', 'Say goodbye to these!', 'This party’s going to be Off. The. Hook.', 'There are dozens of us. Dozens!', 'And that’s why you always leave a note.', 'I’m afraid I just blue myself.', 'There is always money in the banana stand.', 'I’ve made a huge mistake.', 'Dead dove. Do not eat.', 'Here’s some money. Go see a Star War.', 'It’s hot ham water!', 'But where does the lighter fluid come from?', 'Get rid of the Seaward.', 'You’re just a chicken.', 'It’s an illusion Michael!', 'For British eyes only', 'Family love Michael.', 'Watch out for hop-ons.', 'They don’t allow you to have bees here.', 'Has anyone in this family seen a chicken?', 'Solid as a rock!', 'Did nothing cancel?', 'I know you’re the big marriage expert.', 'She calls it a mayonegg.', 'It’s vodka. It goes bad once it’s opened.', 'Don’t call it that.', 'On the Next Arrested Development...', 'Luz, that coat costs more than your house!', 'I just want my kids back.', 'I have Pop Pop in the attic.', 'The soup of the day is Bread.', 'My heart is straining through my shirt', 'Maybe, I’ll put it in her brownie.', 'I like hot sailors.', 'I understand more than you’ll never know.', 'Who’d like a banger in the mouth?', 'And that’s why you don’t yell.', 'I don’t care for GOB.', 'No touching! No touching!', 'Glasses off, hair up.', 'And I think I maced a crane.', 'You’re my third least favorite child.', 'Something that says leather daddy?', 'I enjoy scholarly pursuits.', 'You’re a crook, Captain Hook...', 'And this is not a Volvo.', 'Rita corny, Michael.', 'We’re having a fire sale.', 'Tea for dong!', 'They said it was a bob.']
print(bigram_poem(random.choice(AD)))               # Convert random quote to bigram poem
###                      ###

with open("twitter_credentials.json", "r") as file:                   # load credentials from json file (not included for security reasons)
    creds = json.load(file)

twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
          creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])              # add credentials to access API

class MyStreamer(TwythonStreamer):                                    # create a class that inherits TwythonStreamer
    
    def on_success(self, data):                                       # receive data when successful
                                                                      # Conditions: 1) restrict tweets to 3 or more words,
        tweet = data['text']                                          #    2) exclude retweets, 3) exclude links,
        bigram_len = bigram_poem(tweet).count('\n')                   #    4) English only, 5-6) exclude defined users
        if 'text' in data and bigram_len > 2 and 'RT' not in tweet and 'http' not in bigram_poem(tweet) and data['lang'] == 'en' and data['user']['screen_name'] != 'BigramPoetry' and data['user']['screen_name'] != 'sodnpoo_cams':
            tweet = tweet.replace('\n',' ').replace('VIDEO','')       # remove edge cases with bad formatting
            tweet = tweet.replace(' -',' ').replace(' –',' ').replace(' ‘','')
            tweet = tweet.replace('- ',' ').replace(' /',' ').replace('— ',' ')
            tweet = tweet.replace(': ',' ').replace(':)','').replace('&amp','and')
            poem = 'A Bigram Poem inspired by ' + data['user']['screen_name']  # title line
            poem += ':' + '\n' + bigram_poem(tweet)                   # use bigram_poem function
            poem += '   -' + data['user']['name']                     # signature line
            twitter.update_status(status=poem)                        # tweet out on @BigramPoetry account
            print(poem)                                               # print result, timestamp (for testing)
            print(datetime.datetime.now(), '\n')
            self.disconnect()                                         # stop stream (so old tweets don't dam up)

    def on_error(self, status_code, data):                            # when problem with the API
        print(status_code, data)
        print(datetime.datetime.now())
        self.disconnect()

stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],  # credentials for API streaming
          creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

while True:                                                           # continuosly runs the function
            try:                                                      # attempt to execute the below function
                status_stream = stream.statuses.filter(track='#machinelearning') # start the stream to search for tweet
                time.sleep(900) 
            except:                                                   # when above function fails, print error#print("Unexpected error:", sys.exc_info()[0], datetime.datetime.now())
                time.sleep(900)                                       # waits 15 minutes (900 seconds) before starting over


# In[ ]:




